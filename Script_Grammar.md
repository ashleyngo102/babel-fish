\# Algorithm Executor

\<\!--\* freshness: {  
 owner: 'ywhuang'  
 owner: 'xbid-opt-kir'  
 reviewed: '2022-05-20'  
} \*--\>

\#\# Script Executor

Evaluation pipelines are executing scripts by providing an environment (based on  
\[CustomBiddingWoodshedEvent\](http://cs/symbol:contentads\_xbid.custom\_bidding\_lite.CustomBiddingWoodshedEvent))  
and script itself (in the form of a proto with parsed tree) to a  
\[ScriptExecutor\](https://source.corp.google.com/piper///depot/google3/contentads/xbid/learning/custom/lite/executor/script\_executor.h).  
Executor is responsible for computing the value or providing a meaningful error  
message why the value could not be computed.

Execution happens by recursively traversing the parsed tree and executing each  
command.

NOTE: Script Executor should not be assumed to be stateless (and it is not today  
i.e. unvisited positions tracked). For each new evaluation you should always  
create a new instance of it rather than re-using an existing one. Creating new  
instances is lightweight anyway.

\#\# Goals Executor

Similar to Script Executor, goals executor is also called by evaluation pipeline  
to process Custom Bidding Goals based on provided environment (based on  
\[CustomBiddingWoodshedEvent\](http://cs/symbol:contentads\_xbid.custom\_bidding\_lite.CustomBiddingWoodshedEvent)).

NOTE: Unlike the Script Executor, Goals Executor is stateless.

For a given  
\[CustomBiddingGoals\](http://google3/contentads/xbid/learning/custom/lite/spanner/lite\_schema.proto?q=symbol:%5CbCustomBiddingGoals%5Cb),  
the executor could compute an impression vulue for each goal. Then aggregate all  
generated impression values based on  
\[AggregationType\](http://google3/contentads/xbid/learning/custom/lite/spanner/lite\_schema.proto?q=symbol:%5CbAggregationType%5Cb).

\#\#\# Floodlight Goal

The impression value for a given  
\[FloodlightGoal\](http://google3/contentads/xbid/learning/custom/lite/spanner/lite\_schema.proto?q=symbol:%5CbFloodlightGoal%5Cb)  
is evaluated based on  
\[floodlight\_activity\_id\](http://google3/contentads/xbid/learning/custom/lite/spanner/lite\_schema.proto?q=symbol:%5Cbfloodlight\_activity\_id%5Cb)  
and  
\[floodlight\_attribution\_model\_id\](http://google3/contentads/xbid/learning/custom/lite/spanner/lite\_schema.proto?q=symbol:%5Cbfloodlight\_attribution\_model\_id%5Cb).

See  
\[EvaluateFloodlightGoal\](http://google3/contentads/xbid/learning/custom/lite/executor/goals\_executor.cc?q=symbol:%5CbEvaluateFloodlightGoal%5Cb)  
for detailed logic.

\#\#\# Aggregation Type

The goals executor supports two aggregation types:

\*   \[SUM\_OF\_VALUES\](http://google3/contentads/xbid/learning/custom/lite/spanner/lite\_schema.proto?q=symbol:%5CbSUM\_OF\_VALUES%5Cb):  
   return the sum of the impression values from each goal as the final result.  
\*   \[MAXIMUM\_VALUE\](http://google3/contentads/xbid/learning/custom/lite/spanner/lite\_schema.proto?q=symbol:%5CbSUM\_OF\_VALUES%5Cb):  
   return the maxinum impression value among all goals.

\#\# Script Parser

Custom Bidding is using  
\[Lark\](https://cs.corp.google.com/piper///depot/google3/third\_party/py/lark/)  
parser with simplified  
\[Python3 grammar\](https://cs.corp.google.com/piper///depot/google3/contentads/xbid/learning/custom/lite/executor/model\_parser.py?rcl=288792574\&l=50)  
(\[original Lark grammar\](https://source.corp.google.com/piper///depot/google3/third\_party/py/lark/examples/advanced/python3.lark))  
to parse the script or provide an error of why the given script does not parse  
(errors, or today rather only line and column where parsing failed, are  
extracted from Lark). If successful, parser will output a proto with  
\[Algorithm\](http://cs/symbol:contentads\_xbid.custom\_bidding\_lite.Algorithm) that  
contains a parsed tree (part of  
\[ParseResult\](http://cs/symbol:contentads\_xbid.custom\_bidding\_lite.ParseResult)).  
Algorithm protobuf is an input format for downstream pipelines (i.e. it is used  
directly by ScriptExecutor).

\> NOTE: Grammar is very limited \- it does not even support loops but there is a  
\> reason for that.  
\>  
\> High-level direction is:  
\>  
\> \*   If there is any complex code to write by the customer \- it should be  
\>     exposed through a function that can be simply called (anything that  
\>     requires a loop should be handled by us and exposed this way \- i.e.  
\>     \`total\_conversion\_value(...)\`)  
\>     \*   Customers should be able to use the product even with close to 0  
\>         programming knowledge  
\>     \*   Product should be hard to mis-use  
\> \*   We want predictable runtimes that are somewhat linearly correlated with  
\>     the size of the script (which today is the only control knob we have)  
\>     \*   We don’t charge for running scripts, we don’t have automated way to  
\>         handle abusers (other than manual disallowlisting) but abusing is  
\>         quite hard with all current limitations

I would assume this code should hardly ever be modified except for simple cases  
i.e. adding a newly supported  
\[variable\](http://google3/contentads/xbid/learning/custom/lite/executor/model\_parser.py?l=114-127\&rcl=362550589)  
(i.e. media\\\_plan\\\_id) or adding a newly supported  
\[function\](http://google3/contentads/xbid/learning/custom/lite/executor/model\_parser.py?l=129-147\&rcl=362550589).

Tip: As a principle: we should be following **\*\*Python 3\*\*** semantics across the  
board, both in grammar and in execution logic. When in doubt, check what Python  
3 is doing.

Script parser supports 2 types of inputs:  
\[a file passed through a flag\](http://google3/contentads/xbid/learning/custom/lite/executor/model\_parser.py?q=function:parse\_text\_file)  
or serialized proto  
\[passed directly through stdin\](http://google3/contentads/xbid/learning/custom/lite/executor/model\_parser.py?q=function:parse\_binary\_input).  
Script verification server (the only real direct client, everyone else goes  
through the Script verification server to run the parser) uses stdin / stdout  
communication as it was faster to read CNS files in C++ than Python.

Some issues to be aware of:

\*   All custom variables are required to be prefixed with an underscore to avoid  
   collisions with future variables we may want to add  
\*   We support UTF-8 encoding only  
   \*   UTF-8 BOM sequence is ignored  
       \[here\](http://google3/contentads/xbid/learning/custom/lite/executor/model\_parser.py?l=498\&rcl=362550589) \-  
       it was a surprisingly common case that was breaking Lark parser  
       downstream  
\*   GCS uploads are a little bit of a nightmare  
   \*   I have seen pdfs, word docs, images...  
\*   Indents error were handled by Lark by throwing an exception that did not  
   propagate line and column number  
   \*   It was changed by implementing custom  
       \[indenter\](https://source.corp.google.com/piper///depot/google3/contentads/xbid/learning/custom/lite/executor/model\_parser.py?q=class:PythonIndenter)  
       with different failing logic

\> Tip: If possible, prefer to narrow down the grammar over Static Analyzer  
\> changes (ie. cl/268304436) It is usually much less work to prevent things in  
\> the grammar than to add support in the Static Analyzer for new cases  
\>  
> Tip: If possible, prefer to narrow down the grammar over Static Analyzer  
> changes (ie. cl/268304436) It is usually much less work to prevent things in  
> the grammar than to add support in the Static Analyzer for new cases  
>  
> Also, prefer to catch issues at parsing / static analysis time rather than at  
> runtime (if they don’t use Sandbox, the feedback loop for the customer is much  
> slower).

### Grammar

```python
_INPUT_FILE = flags.DEFINE_string('input_file', '', 'Algo file to parse.')

# The grammar evolved from standard Lark Python 3 grammar through a process
# that included:
# 1) Removing not supported syntax constructs (more details:
# go/custom-bidding-lite-algos-execution#heading=h.rfo9mh3k2lzs)
# 2) Simplifying generated tree by removing redundant nodes (more details:
# go/custom-bidding-lite-algos-execution#heading=h.rtlyvol1eylh)
#
# Optimized and simplified version of the grammar produces minimal parse tree
# to speed up algo execution. Trees generated by below grammar have on average
# 30-40% less nodes than those generated by the non-optimized grammar.
#
# Sample tree before optimization: https://paste.googleplex.com/5806698400841728
# Sample tree after optimization: https://paste.googleplex.com/5348194938519552
#
# Please refer to https://github.com/erezsh/lark/wiki/Tree-Construction
# for basic details on how to shape the tree through the grammar.
# LINT.IfChange
CUSTOM_BIDDING_LITE_OPT_GRAMMAR = r"""
multiline_input: (_NEWLINE | _stmt)*

_stmt: _simple_stmt | compound_stmt
_simple_stmt: small_stmt (";" small_stmt)* ";"? _NEWLINE
?small_stmt: (return_stmt | assignment_stmt)
return_stmt: "return" test
assignment_stmt : CUSTOM_VARIABLE "=" test

?compound_stmt: if_stmt
if_stmt: "if" test ":" suite ("elif" test ":" suite)* ("else" ":" suite)?
?suite: _simple_stmt | _NEWLINE _INDENT _stmt+ _DEDENT

?test: or_test ("if" or_test "else" test)?
?or_test: and_test ("or" and_test)*
?and_test: not_test ("and" not_test)*
?not_test: "not" not_test -> not
         | comparison
?comparison: expr (_comp_op expr)*
?expr: and_expr (_pipe_op and_expr)*
?and_expr: arith_expr (_ampersand_op arith_expr)*
?arith_expr: term (_add_op term)*
?term: factor (_mul_op factor)*
?factor: _factor_op factor | power

!_factor_op: PLUS|MINUS
!_add_op: PLUS|MINUS
!_mul_op: STAR|SINGLE_SLASH|MODULO|DOUBLE_SLASH
!_comp_op: LESS_THAN|MORE_THAN|EQUAL|LESS_THAN_OR_EQUALS|MORE_THAN_OR_EQUALS|DIFFERENT|NOT_EQUAL|NOT_IN|IN
!_ampersand_op: AMPERSAND
!_pipe_op: PIPE

?power: atom_expr ("**" factor)?

?atom_expr: function "(" (_arguments)? ")"     -> funccall
          | atom_expr "[" test "]"             -> getitem
          | atom

?atom: "(" _testlist_comp? ")"     -> tuple
     | "[" _testlist_comp? "]"     -> list
     | "{" dictorsetmaker? "}"     -> dict
     | variable
     | number | string+
     | "(" test ")"
     | "None"    -> const_none
     | "True"    -> const_true
     | "False"   -> const_false

_testlist_comp: test ( ("," test)+ ","? | ",")?
dictmaker: (test ":" test) ("," (test ":" test))* ","?
setmaker: test ("," test)* ","?
?dictorsetmaker: (dictmaker | setmaker)

_arguments: test ("," test)*

// not used in grammar, but may appear in "node" passed from Parser to Compiler
encoding_decl: variable | function

?number: DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT_NUMBER
?string: STRING
?variable: VARIABLE | CUSTOM_VARIABLE
?function: FUNCTION

// Tokens
// NOTE: Beware that when adding a token that is a prefix of another token the
// order should be so that longer token appears first. Keep lists below in
// alphabetical order with the exception for the above rule.
VARIABLE: "active_view_measurable" | "active_view_viewed" | "ad_position"
       | "ad_type" | "advertiser_id" | "adx_page_categories" | "audible"
       | "browser_id" | "browser_reportable_id"
       | "browser_timezone_offset_minutes" | "channels"
       | "city_id" | "click_through_conversion_activity_ids" | "click"
       | "completed_in_view_audible" | "country_code" | "country_id"
       | "creative_id" | "creative_height" | "creative_width" | "date"
       | "day_of_week" | "device_type" | "dma_id" | "domain" | "environment"
       | "exchange_id" | "hour_of_day" | "isp_id" | "isp_reportable_id"
       | "insertion_order_id" | "language" | "line_item_id"
       | "matching_targeted_segments" | "mobile_make_id"
       | "mobile_make_reportable_id" | "mobile_model_id"
       | "mobile_model_reportable_id" | "net_speed" | "operating_system_id"
       | "operating_system_reportable_id" | "partner_id" | "publisher_id"
       | "site_id" | "time_on_screen_seconds" | "url" | "utc_date"
       | "utc_hour_of_day" | "video_completed" | "video_content_duration_bucket"
       | "video_genre_ids" | "video_livestream" | "video_player_height_start"
       | "video_player_size" | "video_player_width_start"
       | "video_resized" | "viewable_on_complete"
       | "view_through_conversion_activity_ids" | "zip_postal_code"

FUNCTION: "bool" | "conversion_variable_num" | "conversion_variable_ord"
       | "conversion_variable_oref" | "conversion_variable_tran"
       | "conversion_variable_u" | "conversion_custom_variable"
       | "first_match_aggregate" | "float" | "ga_goals_count"
       | "ga_goals_max_value" | "ga_goals_total_value" | "ga4_conversions_count"
       | "ga4_conversions_max_value_usd" | "ga4_conversions_max_value"
       | "ga4_conversions_total_value_usd" | "ga4_conversions_total_value"
       | "has_click_through_conversion" | "has_ga_goal" | "has_ga4_conversions"
       | "has_view_through_conversion" | "int" | "log" | "max_aggregate"
       | "str" | "sum_aggregate"
       | "total_conversion_count_micros" | "total_conversion_count"
       | "total_conversion_quantity_micros" | "total_conversion_quantity"
       | "total_conversion_value_micros" | "total_conversion_value"
       | "total_ctc_conversion_count_micros"
       | "total_ctc_conversion_quantity_micros"
       | "total_ctc_conversion_value_micros"
       | "total_vtc_conversion_count_micros"
       | "total_vtc_conversion_quantity_micros"
       | "total_vtc_conversion_value_micros"

// Custom variables are required to be prefixed with underscore to avoid
// name collisions.
CUSTOM_VARIABLE: /_[a-zA-Z_]\w*/

PLUS: "+"
MINUS: "-"
STAR: "*"
SINGLE_SLASH: "/"
DOUBLE_SLASH: "//"
MODULO: "%"
EQUAL: "=="
NOT_EQUAL: "!="
DIFFERENT: "<>"
LESS_THAN: "<"
MORE_THAN: ">"
LESS_THAN_OR_EQUALS: "<="
MORE_THAN_OR_EQUALS: ">="
NOT_IN: /not[\t \f]+in/
IN: "in"
PIPE: "|"
AMPERSAND: "&"
COMMENT: /#[^\n]*/
MULTILINE_COMMENT: "'''" /(.|\n|\r|\t)*/ "'''"
                 | THREE_DOUBLE_QUOTES_TOKEN /(.|\n|\r|\t)*/ THREE_DOUBLE_QUOTES_TOKEN
_NEWLINE: ( /\r?\n[\t ]*/ | COMMENT )+

STRING : /[ubf]?r?("(?!"").*?(?<!\\)(\\\\)*?"|'(?!'').*?(?<!\\)(\\\\)*?')/i

DEC_NUMBER: /0|[1-9]\d*/i
HEX_NUMBER.2: /0x[\da-f]*/i
OCT_NUMBER.2: /0o[0-7]*/i
FLOAT_NUMBER.2: /((\d+\.\d*|\.\d+)(e[-+]?\d+)?|\d+(e[-+]?\d+))/i

%ignore /[\t \f]+/             // WS
%ignore /[\xC2\xA0]/           // NON-BREAKABLE SPACE
%ignore /[\xEF\xBB\xBF]/       // UTF-8 BOM sequence
%ignore /\\[\t \f]*\r?\n/      // LINE_CONT
%ignore COMMENT
%ignore MULTILINE_COMMENT

%declare _INDENT _DEDENT
"""


class UnexpectedIndent(exceptions.ParseError, exceptions.UnexpectedInput):
  """Defines grammar error related to unexpected indent."""

  def __init__(self, line, column, expected):
    self.line = line
    self.column = column
    self.expected = expected

    message = (
        'Unexpected indent in line %s. Found indent of %s.\n'
        'Expected indent of %s\n' % (self.line, self.column, self.expected)
    )

    super(UnexpectedIndent, self).__init__(message)


# This class roughly re-implements the original Lark Indenter class as the
# original one:
# 1) does not track the lines and columns number of misaligned indents
# 2) asserts when there is a misalignemnt instead of raisign a meaningful
#    exception
class PythonIndenter(indenter.Indenter):
  """Defines Python-style indents for Lark library."""

  NL_type = '_NEWLINE'  # pylint: disable=invalid-name
  OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']  # pylint: disable=invalid-name
  CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']  # pylint: disable=invalid-name
  INDENT_type = '_INDENT'  # pylint: disable=invalid-name
  DEDENT_type = '_DEDENT'  # pylint: disable=invalid-name
  tab_len = 8

  def __init__(self):
    self.paren_level = None
    self.indent_level = None
    self.line = 1
    assert self.tab_len > 0

  def handle_NL(self, token):
    self.line += 1

    if self.paren_level > 0:
      return

    yield token

    indent_str = stringutil.ensure_str(token).rsplit('\n', 1)[
        1
    ]  # Tabs and spaces
    indent = indent_str.count(' ') + indent_str.count('\t') * self.tab_len

    if indent > self.indent_level[-1]:
      self.indent_level.append(indent)
      yield lexer.Token.new_borrow_pos(self.INDENT_type, indent_str, token)
    else:
      while indent < self.indent_level[-1]:
        self.indent_level.pop()
        yield lexer.Token.new_borrow_pos(self.DEDENT_type, indent_str, token)

      # Script is ill-formatted if the indents do not match up.
      if indent != self.indent_level[-1]:
        raise UnexpectedIndent(self.line, indent, self.indent_level[-1])

  def _process(self, stream):
    for token in stream:
      if token.type == self.NL_type:
        for t in self.handle_NL(token):
          yield t
      else:
        yield token

      if token.type in self.OPEN_PAREN_types:
        self.paren_level += 1
      elif token.type in self.CLOSE_PAREN_types:
        self.paren_level -= 1
        assert self.paren_level >= 0

    while len(self.indent_level) > 1:
      self.indent_level.pop()
      yield lexer.Token(stringutil.ensure_binary(self.DEDENT_type), '')  # pytype: disable=wrong-arg-types

    if self.indent_level != [0]:
      if not self.indent_level:
        raise UnexpectedIndent(self.line, 0, 0)
      else:
        raise UnexpectedIndent(self.line, self.indent_level[0], 0)

  def process(self, stream):
    self.paren_level = 0
    self.indent_level = [0]
    return self._process(stream)

  # XXX Hack for ContextualLexer. Maybe there's a more elegant solution?
  @property
  def always_accept(self):
    return (self.NL_type,)


# LINT.ThenChange(//depot/google3/contentads/xbid/ui/custom_bidding/script_editor/wrapper/lib/code_mirror_options.dart)
class ModelParser(object):
  """Parses model accroding to Custom Bidding grammar and returns parse tree."""

  def __init__(self, grammar):
    if grammar == lite_pb2.Grammar.LITE_OPTIMIZED:
      # Used lexer is a 'contextual' (as opposed to 'standard') one which as per
      # Lark documentation: "communicates with the parser, and uses the parser's
      # lookahead prediction to narrow its choice of tokens. So at each point,
      # the lexer only matches the subgroup of terminals that are legal at that
      # parser state, instead of all of the terminals."
      self.parser = lark.Lark(
          CUSTOM_BIDDING_LITE_OPT_GRAMMAR.replace(
              'THREE_DOUBLE_QUOTES_TOKEN', '''"\\"\\"\\""'''
          ),
          start='multiline_input',
          lexer='contextual',
          postlex=PythonIndenter(),
          parser='lalr',
          propagate_positions=True,
      )
    else:
      raise Exception('Unsupported grammar.')

  def parse(self, code):
    """Returns raw Lark parse tree for code."""
    return self.parser.parse(code)

  def extract(self, code):
    """Returns code parsed and transformed to lite_pb2.Algorithm proto."""
    parse_tree = self.parse(code)
    algorithm = lite_pb2.Algorithm()
    self._transform(parse_tree, algorithm.root)
    return algorithm

  def _instruction(self, inst):
    """Translates instruction command to corresponding enum value."""
    if inst == 'multiline_input':
      return lite_pb2.Tree.MULTILINE_INPUT
    if inst == 'return_stmt':
      return lite_pb2.Tree.RETURN_STMT
    if inst == 'testlist':
      return lite_pb2.Tree.TESTLIST
    if inst == 'number':
      return lite_pb2.Tree.NUMBER
    if inst == 'arith_expr':
      return lite_pb2.Tree.ARITH_EXPR
    if inst == 'compound_stmt':
      return lite_pb2.Tree.COMPOUND_STMT
    if inst == 'if_stmt':
      return lite_pb2.Tree.IF_STMT
    if inst == 'test':
      return lite_pb2.Tree.TEST
    if inst == 'or_test':
      return lite_pb2.Tree.OR_TEST
    if inst == 'comparison':
      return lite_pb2.Tree.COMPARISON
    if inst == 'suite':
      return lite_pb2.Tree.FUNCCALL
    if inst == 'list':
      return lite_pb2.Tree.LIST
    if inst == 'tuple':
      return lite_pb2.Tree.TUPLE
    if inst == 'var':
      return lite_pb2.Tree.VAR
    if inst == 'name':
      return lite_pb2.Tree.NAME
    if inst == 'power':
      return lite_pb2.Tree.POWER
    if inst == 'term':
      return lite_pb2.Tree.TERM
    if inst == 'not':
      return lite_pb2.Tree.NOT
    if inst == 'string':
      return lite_pb2.Tree.STRING
    if inst == 'dict':
      return lite_pb2.Tree.DICT
    if inst == 'dictmaker':
      return lite_pb2.Tree.DICTMAKER
    if inst == 'setmaker':
      return lite_pb2.Tree.SETMAKER
    if inst == 'getattr':
      return lite_pb2.Tree.GETATTR
    if inst == 'getitem':
      return lite_pb2.Tree.GETITEM
    if inst == 'factor':
      return lite_pb2.Tree.FACTOR
    if inst == 'const_none':
      return lite_pb2.Tree.CONST_NONE
    if inst == 'const_true':
      return lite_pb2.Tree.CONST_TRUE
    if inst == 'const_false':
      return lite_pb2.Tree.CONST_FALSE
    if inst == 'and_test':
      return lite_pb2.Tree.AND_TEST
    if inst == 'not_test':
      return lite_pb2.Tree.NOT_TEST
    if inst == 'simple_stmt':
      return lite_pb2.Tree.SIMPLE_STMT
    if inst == 'small_stmt':
      return lite_pb2.Tree.SMALL_STMT
    if inst == 'assignment_stmt':
      return lite_pb2.Tree.ASSIGNMENT_STMT
    if inst == 'and_expr':
      return lite_pb2.Tree.AND_EXPR
    if inst == 'expr':
      return lite_pb2.Tree.EXPR

    return lite_pb2.Tree.UNDEFINED

  def _token_type(self, token):
    """Translates token type to corresponding enum value."""
    if token == 'DEC_NUMBER':
      return lite_pb2.Token.DEC_NUMBER
    if token == 'HEX_NUMBER':
      return lite_pb2.Token.HEX_NUMBER
    if token == 'OCT_NUMBER':
      return lite_pb2.Token.OCT_NUMBER
    if token == 'FLOAT_NUMBER':
      return lite_pb2.Token.FLOAT_NUMBER
    if token == 'STRING':
      return lite_pb2.Token.STRING
    if token == 'VARIABLE':
      return lite_pb2.Token.VARIABLE
    if token == 'CUSTOM_VARIABLE':
      return lite_pb2.Token.CUSTOM_VARIABLE
    if token == 'FUNCTION':
      return lite_pb2.Token.FUNCTION
    if token == 'PLUS':
      return lite_pb2.Token.PLUS
    if token == 'MINUS':
      return lite_pb2.Token.MINUS
    if token == 'IN':
      return lite_pb2.Token.IN
    if token == 'NOT_IN':
      return lite_pb2.Token.NOT_IN
    if token == 'STAR':
      return lite_pb2.Token.STAR
    if token == 'SINGLE_SLASH':
      return lite_pb2.Token.SINGLE_SLASH
    if token == 'DOUBLE_SLASH':
      return lite_pb2.Token.DOUBLE_SLASH
    if token == 'MODULO':
      return lite_pb2.Token.MODULO
    if token == 'EQUAL':
      return lite_pb2.Token.EQUAL
    # There is hardly any difference between <> and != (actually <> is getting
    # deprecated) so we will use same token for both.
    if token == 'NOT_EQUAL':
      return lite_pb2.Token.NOT_EQUAL
    if token == 'DIFFERENT':
      return lite_pb2.Token.NOT_EQUAL
    if token == 'LESS_THAN':
      return lite_pb2.Token.LESS_THAN
    if token == 'MORE_THAN':
      return lite_pb2.Token.MORE_THAN
    if token == 'LESS_THAN_OR_EQUALS':
      return lite_pb2.Token.LESS_THAN_OR_EQUALS
    if token == 'MORE_THAN_OR_EQUALS':
      return lite_pb2.Token.MORE_THAN_OR_EQUALS
    if token == 'PIPE':
      return lite_pb2.Token.PIPE
    if token == 'AMPERSAND':
      return lite_pb2.Token.AMPERSAND

    return lite_pb2.Token.UNDEFINED

  def _build_position(self, node, position):
    """Builds position for a node."""

    # meta will only be accessed if node.line and node.column are not set.
    # therefore no need to check for meta is not None
    meta = getattr(node, '_meta', None)

    if hasattr(node, 'line') and node.line is not None:
      position.line = node.line
    elif meta is not None and hasattr(meta, 'line') and meta.line is not None:
      position.line = meta.line
    else:
      position.line = 1

    if hasattr(node, 'column') and node.column is not None:
      position.column = node.column
    elif (
        meta is not None and hasattr(meta, 'column') and meta.column is not None
    ):
      position.column = meta.column
    else:
      position.column = 1

    # end_line and end_column can be set on the node or the node._meta.
    if hasattr(node, 'end_line') and node.end_line is not None:
      position.end_line = node.end_line
    elif (
        meta is not None
        and hasattr(meta, 'end_line')
        and meta.end_line is not None
    ):
      position.end_line = meta.end_line

    if hasattr(node, 'end_column') and node.end_column is not None:
      position.end_column = node.end_column
    elif (
        meta is not None
        and hasattr(meta, 'end_column')
        and meta.end_column is not None
    ):
      position.end_column = meta.end_column

  def _build_tree(self, node, input_tree):
    input_tree.instruction = self._instruction(node.data)
    for child in node.children:
      tree_or_token = input_tree.children.add()
      self._transform(child, tree_or_token)
    self._build_position(node, input_tree.position)

  def _build_token(self, node, token):
    token.value.string_value = node.value
    token.type = self._token_type(node.type)
    self._build_position(node, token.position)

  def _transform(self, node, root):
    """Transforms Lark tree into the wrapper lite_pb2.TreeOrToken format."""
    if isinstance(node, tree.Tree):
      self._build_tree(node, root.tree)
      return

    if isinstance(node, lexer.Token):
      self._build_token(node, root.token)
      return

    raise Exception('Transformation failed.')

  def _build_error(self, error_code, exception, parse_result):
    """Builds error_summary by exception."""
    parse_result.ClearField('algorithm')
    parse_result.error_summary.error_code = error_code
    parse_result.error_summary.error_message = str(exception)
    parse_result.error_summary.position.line = exception.line
    parse_result.error_summary.position.column = exception.column

  def parse_algo(self, code, parse_result):
    """Builds parse_result by parsed code or parsing errors."""
    try:
      # Parser requires the script to end with newline. Always add one in case
      # original script does not have it. We don't want to fail parsing for
      # such a trivial reason. Characters like BOM UTF-8 sequence fail the
      # parser, ignore these characters.
      code = stringutil.ensure_str(code, 'utf-8-sig', 'ignore') + '\n'
      parse_tree = self.parse(code)
      self._transform(parse_tree, parse_result.algorithm.root)
    except exceptions.UnexpectedToken as error:
      self._build_error(
          lite_pb2.FailedParseSummary.GRAMMAR_ERROR, error, parse_result
      )
    except UnexpectedIndent as error:
      self._build_error(
          lite_pb2.FailedParseSummary.GRAMMAR_ERROR, error, parse_result
      )
    except exceptions.UnexpectedCharacters as error:
      self._build_error(
          lite_pb2.FailedParseSummary.TOKEN_ERROR, error, parse_result
      )


def write_parse_result(result):
  """Writes result to stdout as serialized string."""
  # Workaround for issue when exiting Python process reports:
  #   close failed in file object destructor:
  #   sys.excepthook is missing
  #   lost sys.stderr
  # as suggested in: https://bugs.python.org/issue11380
  # Workaround turns it into regular "Broken pipe error" which we can catch and
  # handle (or ignore in this case). Broken pipe may happen on flush as parent
  # process might have already closed its end of stdout earlier.
  try:
    sys.stdout.buffer.write(result.SerializeToString())
    sys.stdout.buffer.flush()
  except IOError:
    pass
  finally:
    sys.stdout.close()


def write_failed_parse_result(error_code):
  """Creates result for a failed parsing and writes it to stdout."""
  parse_result = lite_pb2.ParseResult()
  parse_result.error_summary.error_code = error_code
  write_parse_result(parse_result)


def parse_binary_input(parser):
  """Parses serialized proto with code read from stdin."""
  length_bytes = sys.stdin.buffer.read(4)
  if not length_bytes or len(length_bytes) != 4:
    write_failed_parse_result(lite_pb2.FailedParseSummary.MALFORMED_REQUEST)
    return

  # This depends on running on a platform with 32-bit unsigned int type.
  # The Python struct module unfortunately has no format specifier for uint32_t.
  length = struct.unpack('<I', length_bytes)[0]
  serialized_request = sys.stdin.buffer.read(length)
  if len(serialized_request) != length:
    write_failed_parse_result(lite_pb2.FailedParseSummary.MALFORMED_REQUEST)
    return

  request = lite_pb2.ParseRequest()
  request.ParseFromString(serialized_request)

  parse_result = lite_pb2.ParseResult()
  parser.parse_algo(request.code.encode('utf-8', 'ignore'), parse_result)
  write_parse_result(parse_result)


def parse_text_file(parser, filepath):
  """Parses file under filepath and returns results to stdout."""
  parse_result = lite_pb2.ParseResult()
  if gfile.Exists(filepath):
    with gfile.Open(filepath, 'rt', encoding='utf-8-sig') as algo_file:
      code = algo_file.read()
    parser.parse_algo(code, parse_result)
  else:
    parse_result.error_summary.error_code = (
        lite_pb2.FailedParseSummary.FILE_NOT_FOUND
    )

    parse_result.error_summary.error_message = (
        'Algorithm file not found at %s' % filepath
    )

  # Outputs parser result to stdout, which connects to verification service by
  # PIPE.
  write_parse_result(parse_result)


def main(argv):
  del argv  # Unused

  parser = ModelParser(lite_pb2.Grammar.LITE_OPTIMIZED)

  if not _INPUT_FILE.value:
    parse_binary_input(parser)
    return

  parse_text_file(parser, _INPUT_FILE.value)
  return


if __name__ == '__main__':
  app.run(main)
```
