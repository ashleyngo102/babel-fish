# Custom bidding script reference

You can use functions and signals to create a custom bidding script. This script will help build your custom bidding model by improving your target key performance indicators (KPIs).

On this page

* [Syntax rules](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#syntax-rules)  
  * [Comments](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#Comments)  
  * [Operators](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#Operators)  
* [Available functions and signals](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#available-functions-signals)  
  * [Functions](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#available-functions)  
  * [Signals](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#available-signals)  
  * [Google Analytics](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#google-analytics-signals)  
* [Limitations](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#limitations)

## Syntax rules

You can improve impression values by using first-party data to inform your custom bidding scripts. Display & Video 360 supports first-party data from:

* [Floodlights](https://support.google.com/displayvideo/answer/11969760)  
* [Impression level data](https://support.google.com/displayvideo/answer/11968381)  
* [Google Analytics](https://support.google.com/displayvideo/answer/11969662)

When you [create a custom bidding script](https://support.google.com/displayvideo/answer/9728993), you’ll use the following syntax rules:

* Enclose all criteria in brackets \[ \]  
* A comma , also represents "and"

Example  
In this sample script, criteria1 returns true only if criteria\_a and criteria\_b are both true. While criteria2 returns true if criteria\_a is true:  
return aggregate\_function(\[  
(\[criteria\_a, criteria\_b\], score), \#criteria1  
(\[criteria\_a\], score) \#criteria2  
\])

### Comments

You can use comments to add context to your script. For example, you can add comments to communicate the intent of your script.

You can use the following syntax for comments:

* To add a single-line comment, use \#.  
* To add a multi-line comment, enclose your comment in """ or '''.

Example

\# This is an single line comment

"""

This is a multi-line comment

"""

'''

This is also a multi-line comment

'''

### Operators

You can use the following operators in your script:

* Arithmetic operators: \+ , \-, \*, / , %, \*\*, //  
* Assignment operators: \=, \+=, \-=, \*=, /=, %=, \*\*=, //=  
* Comparison operators: \==, \!=, \<, \>, \>=, \<=  
* Logical operators: and, or, not  
* Membership operators: in, not in

#### Membership operators

You can use the in and not in membership operators in your script to check whether an element is in a field or not.

* in: Returns true if the element is found in the field.  
* not in: Returns true if the element is not found in the field.

Example  
if 123 in channel\_id: \#checks if 123 is in the channel ID  
return y

#### Comparison operators

You can use comparison operators to include or exclude an element from your model.

Example 1  
The following script excludes a date from your custom bidding model:

\# Excluding date

if date \== 20180711:

return None

You can identify impressions you want to exclude when training your custom bidding model by returning None. You can use a statement that returns None to identify impressions you want excluded when training your custom bidding model.

Example 2

The following script excludes an ad type from your custom bidding model:

\# Excluding slice (ad\_type \== 1 means VIDEO)

if ad\_type \!= 1:

return None

## Available functions and signals

The following is a list of functions you can use in your custom bidding script. The tables contain the following information:

* Field: The function or signal name you use in the script.  
* Type: The output data type. Custom bidding supports the following data types:  
  * Boolean: Contains a true or a false value.  
  * Binary: Contains binary data.  
  * Double: Contains a floating numerical value. For example, 1.0 .  
  * List of integers: Contains a set of integers.  
  * Integer: Contains positive or negative whole numbers. For example, 1 or \-1.  
  * String: Contains UTF-8 characters from a minimum length of 0 or more. For example, country\_code outputs a string “US”.  
* Details: Contains more information and link to examples.

For more details, go to the [Display & Video 360 API](https://developers.google.com/display-video/api/reference/rest) or download the [Structured Data File (SDF)](https://developers.google.com/display-video/api/guides/downloading-sdfs/create).

### Functions

Display & Video 360 custom bidding supports the following functions:

* [Aggregate](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#aggregate-functions): Functions that calculate aggregated values assigned to a criteria.  
* [Casting](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#casting-functions): Functions that convert a variable to a specific data type to perform an operation.  
* [Math](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#math-functions): Functions that calculate values using advanced math.

These functions accept one or more [signals](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#available-signals) to accurately represent your key performance indicators (KPIs) in your custom bidding script.

| Category | Function | Type | Details |
| :---- | :---- | :---- | :---- |
| **Aggregate functions** | first\_match\_aggregate | Double | Returns the weight value assigned to the first criteria in the array that returns true. |
|  | max\_aggregate | Double | Returns the highest weight value assigned to criteria that returns true. |
|  | sum\_aggregate | Double | Returns the sum of all values assigned to all criteria that return true. |
| **Casting functions** | bool | bool(x) | Returns a boolean value: true or false. |
|  | float | float(x) | Converts a number or a string data type: Returns a floating point. Example: float(1) returns as 1.0. |
|  | int | int(x) | Converts a number or a string data type and returns an integer. Example: int(1.0) returns as 1. |
|  | str | str(object) | Converts a data type and returns a string. Example: str(1) returns as “1”. |
| **Math functions** | log | log(x\[, base\]) | With one argument: Returns the natural logarithm of x (to base e). With two arguments: Returns the logarithm of x to the given base, calculated as log(x)/log(base). |

### Signals

Display & Video 360 custom bidding functions accept data from the following signal categories:

* [Dimension variables](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#dimension-variable-signals): Signals used in scripts that score based on a variable.  
* [Conversions](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#conversion-signals): Signals used in scripts that score based on a conversion outcome.  
* [Google Analytics](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#google-analytics-signals): Signals used in scripts that score based on data from Google Analytics.

#### Dimension variables

| Category | Signal | Type | Details |
| :---- | :---- | :---- | :---- |
| **General** | advertiser\_id | Integer | The advertiser identifier from Display & Video 360\. |
|  | insertion\_order\_id | Integer | The insertion order identifier from Display & Video 360\. |
|  | line\_item\_id | Integer | The line item identifier from Display & Video 360\. |
| **Date/Time** | date | Integer | The date the impression was made. Format: yyyymmdd |
|  | day\_of\_week | Integer | The numerical code for the day of the week the impression was made. 0 for Sunday 1 for Monday 2 for Tuesday 3 for Wednesday 4 for Thursday 5 for Friday 6 for Saturday |
|  | hour\_of\_day | Integer | The hour the impression was made using the browser's local time zone in the 24-hour format. Valid inputs: 0 \- 23 |
|  | utc\_date | Integer | The date the impression was made using coordinated universal time (UTC). Format: yyyymmdd |
|  | utc\_hour\_of\_day | Integer | The hour the impression was made using coordinated universal time (UTC) in 24-hour format. Valid inputs: 0 \- 23 |
| **Location** | city\_id | Integer | The city identifier. You can generate the city\_id using the [Display & Video 360 API](https://developers.google.com/display-video/api/reference/rest) or by [downloading the SDF metadata](https://support.google.com/displayvideo/answer/6301070). |
|  | country\_code | String | The country or region code. You can [download a pdf of the country or region code mappings](https://storage.googleapis.com/support-kms-prod/8cJKvMpQIKLP0pVran4OjW5cF87n2bxHTapH) as reference. |
|  | country\_id | Integer | The country or region identifier. You can [download a pdf of the country or region ID mappings](https://storage.googleapis.com/support-kms-prod/8cJKvMpQIKLP0pVran4OjW5cF87n2bxHTapH) as reference. |
|  | dma\_id | Integer | The designated market area (DMA) identifier.Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. |
|  | zip\_postal\_code | String | The ZIP or postal code. You can find a list of available ZIP or postal code using the [Display & Video 360 API](https://developers.google.com/display-video/api/reference/rest) or by [downloading the SDF metadata](https://support.google.com/displayvideo/answer/6301070). |
| **Creative (General)** | ad\_type | Integer | The numerical code representing the ad format: 0 for display 1 for video 2 for audio |
|  | creative\_height | Integer | Creative height in pixels. Note: For display creatives only. |
|  | creative\_id | Integer | The creative ID as it appears in Display & Video 360\. |
|  | creative\_width | Integer | Creative width in pixels. Note: For display creatives only. |
| **Computer System** | browser\_reportable\_id | Integer | The browser identifier. Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. Use the public API ID. You can also find the ID in the latest SDF meta file, or using data transfer files. Note: browser\_id was migrated to browser\_reportable\_id in the third quarter of 2025 to align ID spaces across Display & Video 360\. Old scripts created before will be supported for a period of time allowing for users to migrate. |
|  | browser\_timezone\_offset\_minutes | Integer | The difference in minutes between the active time zone on the browser and GMT-12. Example: 1320 represents a browser time zone of GMT+10 |
|  | device\_type | Integer | The numerical code representing the device type: 0 for desktop 1 for unknown 2 for smart phone 3 for tablet 4 for smart TV 5 for connected TV 6 for set top box 7 for connected device |
|  | environment | Integer | The numerical code representing the serving environment for your ad. 10 for web optimized for device 11 for web not optimized for device 12 for app |
|  | isp\_reportable\_isp | Integer | The internet service provider (ISP) identifier. Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. Use the public API ID. You can also find the ID in the latest SDF meta file, or using data transfer files. Note: isp\_id was migrated to isp\_reportable\_id in the third quarter of 2025 to align ID spaces across Display & Video 360\. Old scripts created before will be supported for a period of time allowing for users to migrate. |
|  | language | String | The browser's language setting.Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. |
|  | mobile\_make\_reportable\_id | Integer | The mobile make identifier. Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. Use the public API ID. You can also find the ID in the latest SDF meta file, or using data transfer files. Note: mobile\_make\_id was migrated to mobile\_make\_reportable\_id in the third quarter of 2025 to align ID spaces across Display & Video 360\. Old scripts created before will be supported for a period of time allowing for users to migrate. |
|  | mobile\_model\_reportable\_id | Integer | The mobile model identifier. Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. Use the public API ID. You can also find the ID in the latest SDF meta file, or using data transfer files. Note: mobile\_model\_id was migrated to mobile\_model\_reportable\_id in the third quarter of 2025 to align ID spaces across Display & Video 360\. Old scripts created before will be supported for a period of time allowing for users to migrate. |
|  | net\_speed | Integer | The numerical code representing the network speed detected when the impression was made: 1 for broadband/4G (2mbps and faster) 2 for dialup (56kbps and slower) 3 for unknown connection speed 4 for EDGE/2G (57kbps and faster) 5 for UMTS/3G (384kbps and faster) 6 for basic DSL (768kbps and faster) 7 for HSDPA/3.5G (1.8mbps and faster) |
|  | operating\_system\_reportable\_id | Integer | The operating system identifier. Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. Use the public API ID. You can also find the ID in the latest SDF meta file, or using data transfer files Note: operating\_system\_id was migrated to operating\_system\_reportable\_id in the third quarter of 2025 to align ID spaces across Display & Video 360\. Old scripts created before will be supported for a period of time allowing for users to migrate. |
| **Serving (General)** | ad\_position | Integer | The numerical code representing the ad placement position: 0 for unknown position 1 for above the fold 2 for below the fold |
|  | adx\_page\_categories | List of integers | The page category identifier. You can view the full list category ID mappings on the [AdWords API reference](https://developers.google.com/adwords/api/docs/appendix/verticals). |
|  | channels | List of integers | The channel identifier from Display & Video 360\. |
|  | domain | String | Note: Domains aren't supported for CTV line items. For CTV line items use site\_id. The root domain name which consists of the domain name and the top-level domain. This signal maps to the reporting dimension app/URL. Example: For the URL http://www.domain.com, the root domain would be domain.com. |
|  | exchange\_id | Integer | The exchange identifier.Download the [custom bidding ID sheet (.xlsx format)](https://storage.googleapis.com/support-kms-prod/ItunR3x2VSY67ztAJe24BuhvAF7WJmF6m9sk) for these IDs. |
|  | site\_id | Integer | The site identifier. This signal maps to the reporting dimension app/URL ID. |
| **Active View** | active\_view\_measurable | boolean | Returns 1 for true if the impression was measurable by Active View when your ad was served. Some factors may prevent impressions from being counted. If the impression was not measurable, returns 0 for false. |
|  | active\_view\_viewed | boolean | Returns 1 for true once Active View detects that your ad has been viewed. Otherwise, returns 0 for false. |
| **Event** | click | boolean | Returns 1 for true if the ad was clicked. Otherwise, returns 0 for false. |
|  | time\_on\_screen\_seconds | Integer | The time the ad was on screen in seconds. |
| **Video**   | audible | boolean | Note: Supported for real-time bidding (RTB) videos only Returns 1 for true if the video’s sound was ON when viewed. Otherwise, returns 0 for false. |
|  | completed\_in\_view\_audible | boolean | Note: Supported for real-time bidding (RTB) videos only Returns 1 for true if the video had the sound ON when viewed. Otherwise, returns 0 for false. |
|  | video\_completed | boolean | Note: Only applies to video ad types. Non-video impressions won’t be labeled. Returns 1 for true if the video was completed. Otherwise, returns 0 for false. |
|  | video\_player\_height\_start | Integer | The video player height at first frame in pixels. |
|  | video\_player\_size | Integer | The numerical code representing the target video inventory based on the video player size. 0 for unknown 1 for small 2 for large 3 for high definition (HD) To learn more, go to [Video Targeting](https://support.google.com/displayvideo/answer/6008366). |
|  | video\_player\_width\_start | Integer | The video player width at first frame in pixels. |
|  | video\_resized | Binary | Returns 1 for true if the video player was resized during playback. Otherwise, returns 0 for false. |
|  | viewable\_on\_complete | boolean | Note: Supported for real-time bidding (RTB) videos only. Returns 1 for true if the video was viewed on completion. Otherwise, returns 0 for false. |
|  | video\_content\_duration\_bucket | Integer | Note: Only applies to video ad types. Non-video impressions won’t be labeled. The numerical code that represents the video’s bucket,which is used to categorize videos based on their length. The upper bound range is exclusive. For videos that have a duration of 1 minute: They’re categorized under the “1 to 5 minutes” bucket. They are not under the “0-1 minute” bucket since this bucket excludes videos that are 1 minute or over. Example 0 for unknown 1 for 0 to 1 minute 2 for 1 to 5 minutes 3 for 5 to 15 minutes 4 for 15 to 30 minutes 5 for 30 to 60 minutes 7 for over 60 minutes |
|  | video\_genre\_ids | List of integers | Note: Only applies to video ad types. Non-video impressions won’t be labeled. Represents a list of [video genre IDs](https://support.google.com/displayvideo/answer/11967043?hl=en&visit_id=639117836241284824-1994966723&rd=1#Video-genre-mapping) for targeting ads based on related groups of audio and video inventory. Learn more about [Genre targeting](https://support.google.com/displayvideo/answer/13610700). |
|  | video\_livestream | boolean | Note: Only applies to video ad types. Non-video impressions won’t be labeled. Returns true if the video is a livestream. Otherwise returns false. |

Note: browser\_id, isp\_id, mobile\_make\_id, mobile\_model\_id, and operating\_system\_id are no longer supported. Update your scripts to use browser\_reportable\_id, isp\_reportable\_id, mobile\_make\_reportable\_id, mobile\_model\_reportable\_id, and operating\_system\_reportable\_id instead. This change aligns the ID spaces used in custom bidding with the rest of Display & Video 360, including the latest SDF files, API, and Data Transfer v2.

#### Conversions

| Category | Signal | Type | Details |
| :---- | :---- | :---- | :---- |
| **Conversion signals** | total\_conversion\_count(Floodlight Activity ID, Attribution Model ID) | Double | The total number of conversion events for ID pair. Use your own model, or enter 0 for the model ID to use last-touch attribution. |
|  | total\_conversion\_value(Floodlight Activity ID, Attribution Model ID) | Double | Takes the revenue value from activities tracked by [Floodlight Sales tags](https://support.google.com/tagmanager/answer/6107160). Use your own model, or enter 0 for the model ID to use last-touch attribution. |
|  | total\_conversion\_quantity(FloodlightActivity ID, Attribution Model ID) | Double | The total quantity of conversions attributed to the given ID pair. Use your own model, or enter 0 for the model ID to use last-touch attribution. |
|  | conversion\_custom\_variable(Floodlight Activity ID, Attribution Model ID, Custom Variable Index) | String | The string value of the custom variable for the latest attributed conversion for the impression. Otherwise returns None (if there's no conversion or the value isn't set). Use your own model, or enter 0 for the model ID to use last-touch attribution. |
|  | conversion\_variable\_num(FloodlightActivity ID, Attribution Model ID) | Integer | Gets the latest conversion with positive credit to get the “num” Floodlight variable if it exists where count\_micros is positive. Otherwise returns None. |
|  | conversion\_variable\_ord(Floodlight Activity ID, Attribution Model ID) | String | Gets the latest conversion with positive credit to get the “ord” Floodlight variable if it exists where count\_micros is positive. Otherwise returns None. |

#### Video genre mappings

| Genre ID | Genre Name |
| :---- | :---- |
| 2 | /Adult |
| 3 | /Arts & Entertainment |
| 317 | /Arts & Entertainment/Comics & Animation/Anime & Manga |
| 319 | /Arts & Entertainment/Comics & Animation/Cartoons |
| 1108 | /Arts & Entertainment/Entertainment Industry/Film & TV Industry/Film & TV Awards |
| 569 | /Arts & Entertainment/Events & Listings |
| 1273 | /Arts & Entertainment/Events & Listings/Live Sporting Events |
| 895 | /Arts & Entertainment/Humor/Live Comedy |
| 1097 | /Arts & Entertainment/Movies/Action & Adventure Films |
| 1099 | /Arts & Entertainment/Movies/Action & Adventure Films/Western Films |
| 1095 | /Arts & Entertainment/Movies/Comedy Films |
| 615 | /Arts & Entertainment/Movies/Horror Films |
| 1105 | /Arts & Entertainment/Movies/Musical Films |
| 1310 | /Arts & Entertainment/Movies/Romance Films |
| 616 | /Arts & Entertainment/Movies/Science Fiction & Fantasy Films |
| 1096 | /Arts & Entertainment/Movies/Thriller, Crime & Mystery Films |
| 35 | /Arts & Entertainment/Music & Audio |
| 449 | /Arts & Entertainment/Offbeat/Occult & Paranormal |
| 23 | /Arts & Entertainment/Performing Arts |
| 894 | /Arts & Entertainment/Performing Arts/Acting & Theater |
| 581 | /Arts & Entertainment/Performing Arts/Dance |
| 1185 | /Arts & Entertainment/Performing Arts/Opera |
| 358 | /Arts & Entertainment/TV & Video/TV Shows & Programs |
| 1047 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Comedies |
| 1411 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Documentary & Nonfiction |
| 1193 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Dramas |
| 1111 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Dramas/TV Crime & Legal Shows |
| 357 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Dramas/TV Soap Operas |
| 1110 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Family-Oriented Shows |
| 1050 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Game Shows |
| 1049 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Reality Shows |
| 1112 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Sci-Fi & Fantasy Shows |
| 1410 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Talent & Variety Shows |
| 1048 | /Arts & Entertainment/TV & Video/TV Shows & Programs/TV Talk Shows |
| 24 | /Arts & Entertainment/Visual Art & Design |
| 47 | /Autos & Vehicles |
| 1191 | /Autos & Vehicles/Bicycles & Accessories |
| 1405 | /Autos & Vehicles/Bicycles & Accessories/Mountain Bikes |
| 273 | /Autos & Vehicles/Motor Vehicles (By Type)/Motorcycles |
| 148 | /Autos & Vehicles/Motor Vehicles (By Type)/Off-Road Vehicles |
| 185 | /Beauty & Fitness/Fashion & Style |
| 94 | /Beauty & Fitness/Fitness |
| 241 | /Beauty & Fitness/Fitness/Bodybuilding |
| 1418 | /Beauty & Fitness/Fitness/Fitness Instruction & Personal Training |
| 46 | /Business & Industrial/Agriculture & Forestry |
| 5 | /Computers & Electronics |
| 122 | /Food & Drink/Cooking & Recipes |
| 39 | /Games/Card Games |
| 924 | /Games/Card Games/Poker & Casino Games |
| 924 | /Games/Card Games/Poker & Casino Games |
| 41 | /Games/Computer & Video Games |
| 698 | /Games/Gambling/Sports Betting/Horse & Dog Racing |
| 939 | /Games/Table Games/Billiards |
| 940 | /Games/Table Games/Table Tennis |
| 45 | /Health |
| 284 | /Hobbies & Leisure/Crafts |
| 688 | /Hobbies & Leisure/Outdoors |
| 462 | /Hobbies & Leisure/Outdoors/Fishing |
| 461 | /Hobbies & Leisure/Outdoors/Hunting & Shooting |
| 461 | /Hobbies & Leisure/Outdoors/Hunting & Shooting |
| 461 | /Hobbies & Leisure/Outdoors/Hunting & Shooting |
| 999 | /Hobbies & Leisure/Recreational Aviation |
| 678 | /Hobbies & Leisure/Special Occasions/Holidays & Seasonal Events |
| 459 | /Hobbies & Leisure/Water Activities/Boating |
| 11 | /Home & Garden |
| 158 | /Home & Garden/Home Improvement |
| 966 | /Law & Government/Government/State & Local Government |
| 75 | /Law & Government/Legal |
| 366 | /Law & Government/Military |
| 16 | /News |
| 784 | /News/Business News |
| 396 | /News/Politics |
| 1201 | /News/Politics/Opinion & Commentary |
| 1077 | /News/Sports News |
| 785 | /News/Technology News |
| 63 | /News/Weather |
| 113 | /People & Society/Ethnic & Identity Groups/Lesbian, Gay, Bisexual & Transgender |
| 58 | /People & Society/Family & Relationships/Family/Parenting |
| 59 | /People & Society/Religion & Belief |
| 870 | /People & Society/Self-Help & Motivational |
| 57 | /People & Society/Social Issues & Advocacy/Charity & Philanthropy |
| 82 | /People & Society/Social Issues & Advocacy/Green Living & Environmental Issues |
| 886 | /Pets & Animals/Pets/Dogs |
| 888 | /Pets & Animals/Pets/Horses |
| 119 | /Pets & Animals/Wildlife |
| 119 | /Pets & Animals/Wildlife |
| 690 | /Reference/General Reference/Biographies & Quotations |
| 694 | /Reference/General Reference/How-To, DIY & Expert Content |
| 433 | /Reference/Humanities/History |
| 1288 | /Reference/Humanities/History/Military History |
| 174 | /Science |
| 18 | /Shopping |
| 64 | /Shopping/Antiques & Collectibles |
| 292 | /Shopping/Auctions |
| 69 | /Shopping/Consumer Resources |
| 1666 | /Sports/Animal Sports |
| 568 | /Sports/Animal Sports/Equestrian |
| 515 | /Sports/Combat Sports/Boxing |
| 516 | /Sports/Combat Sports/Martial Arts |
| 1674 | /Sports/Combat Sports/Martial Arts/Mixed Martial Arts |
| 512 | /Sports/Combat Sports/Wrestling |
| 1681 | /Sports/Combat Sports/Wrestling/Professional Wrestling |
| 554 | /Sports/Extreme Sports |
| 1206 | /Sports/Extreme Sports/Drag & Street Racing |
| 1000 | /Sports/Individual Sports |
| 1016 | /Sports/Individual Sports/Bowling |
| 458 | /Sports/Individual Sports/Cycling |
| 261 | /Sports/Individual Sports/Golf |
| 519 | /Sports/Individual Sports/Gymnastics |
| 262 | /Sports/Individual Sports/Racquet Sports |
| 1376 | /Sports/Individual Sports/Racquet Sports/Tennis |
| 541 | /Sports/Individual Sports/Running & Walking |
| 1126 | /Sports/Individual Sports/Skate Sports |
| 518 | /Sports/Individual Sports/Track & Field |
| 513 | /Sports/International Sports Competitions/Olympics |
| 180 | /Sports/Motor Sports |
| 1595 | /Sports/Motor Sports/Auto Racing |
| 1596 | /Sports/Motor Sports/Motorcycle Racing |
| 1001 | /Sports/Team Sports |
| 258 | /Sports/Team Sports/American Football |
| 259 | /Sports/Team Sports/Baseball |
| 264 | /Sports/Team Sports/Basketball |
| 534 | /Sports/Team Sports/Cheerleading |
| 296 | /Sports/Team Sports/Cricket |
| 1017 | /Sports/Team Sports/Handball |
| 260 | /Sports/Team Sports/Hockey |
| 517 | /Sports/Team Sports/Rugby |
| 294 | /Sports/Team Sports/Soccer |
| 699 | /Sports/Team Sports/Volleyball |
| 118 | /Sports/Water Sports |
| 1593 | /Sports/Water Sports/Surfing |
| 1594 | /Sports/Water Sports/Swimming |
| 265 | /Sports/Winter Sports |
| 1149 | /Sports/Winter Sports/Ice Skating |
| 1148 | /Sports/Winter Sports/Skiing & Snowboarding |
| 67 | /Travel & Transportation |

### Google Analytics

Important  
To use Google Analytics conversions to inform your custom bidding model, you'll need to share conversion data. Learn more [About linking Google Analytics 4 to Display & Video 360](https://support.google.com/displayvideo/answer/11356656).

| Category | Signal | Type | Details |
| :---- | :---- | :---- | :---- |
| **Google Analytics** | has\_ga4\_conversions(property\_id, conversion\_event\_name) | Boolean | Returns true if a given impression has at least one conversion with a property ID and conversion event attributed. Otherwise returns false. |
|  | ga4\_conversions\_count(property\_id, conversion\_event\_name) | Integer | Returns the number of conversions with a property ID and conversion event attributed to the given impression. |
|  | ga4\_conversions\_max\_value(property\_id,conversion\_event\_name))\* | Double | Returns the highest value assigned to a conversion with a property ID and conversion event attributed to the given impression. Returns 0 if the highest conversion value is 0 or if no conversions are attributed. |
|  | ga4\_conversions\_max\_value\_usd(property\_id, conversion\_event\_name) | Double | Note: For Google Analytics accounts using USD currency. Returns the highest value assigned to a conversion with a property ID and conversion ID attributed to the given impression Returns 0 if the highest conversion value is 0 or if no conversions are attributed. |
|  | ga4\_conversions\_total\_value(GA4 property ID, conversion\_event\_name) | Double | Returns the sum of the weight values assigned to conversions with a property ID and conversion event attributed to the given impression. Returns 0 if the highest conversion value is 0 or if no conversions are attributed. |
|  | ga4\_conversions\_total\_value\_usd(property\_id, conversion\_event\_name) | Double | Note: For Google Analytics accounts using USD currency. Returns the sum of the weight values assigned to conversions with a property ID and conversion event attributed to the given impression. Returns 0 if the highest conversion value is 0 or if no conversions are attributed. |

## Limitations

The following aren’t supported in custom bidding scripts:

* Passing named arguments: For example, func(arg1 \= “abc”, arg2 \= “def”)  
* Subscripts and slices: For example, userlists\[1:3\]  
* Referencing attributes: For example, domain.length  
* Variable and function names can come from a predefined set  
* Recursion  
* Advanced custom variable assignments:  
  * multi assignments  
  * augmented assignments  
  * annotated assignments

Example

The following are samples of unsupported syntax in custom variable assignments

\_a, \_b \= 1, 2

\_a, \_b \= \_b, \_a

\_a \= \_b \= 2

\_idx \+= 1

* Unsupported keywords:  
  * global, nonlocal and exec keywords  
  * class and class definitions  
  * def and function definitions  
  * Import and import from keywords  
  * lambda and lambdas support  
  * break  
  * continue  
  * yield  
  * raise  
  * assert  
  * try  
  * finally  
  * except  
  * async  
  * await  
  * del  
  * Pass  
  * ellipsis  
* Unsupported loops:  
  * for and while loops.  
* Unsupported operators:  
  * \* and \*\* when used in non-arithmetic statements.  
  * \<\< and \>\> shift operators.  
  * Bit operators  
  * @ decorators.  
  * is, not is identity operators

