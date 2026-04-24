# Custom bidding overview

Custom bidding lets you use your business insights and Google’s AI technology to automate how you achieve your campaign goals while maximizing your return on ad spend.

You can reach your campaign goals by optimizing your bids for specific conversion events, goals, or impression signals that are more valuable to you. You can use custom bidding with signals from:

* Floodlight events and custom Floodlight variables  
* Google Analytics 4  
* Impression signals

#### Topics in this article

* [How custom bidding works](https://support.google.com/displayvideo/answer/9723477?sjid=643040824425448523-NC#how-it-works)  
  * [Examples](https://support.google.com/displayvideo/answer/9723477?sjid=643040824425448523-NC#examples)  
  * [Summary insights](https://support.google.com/displayvideo/answer/9723477?sjid=643040824425448523-NC#Summary_insights)  
* [Permission and access](https://support.google.com/displayvideo/answer/9723477?sjid=643040824425448523-NC#permissions-custom-bidding)  
* [Custom bidding support limitations](https://support.google.com/displayvideo/answer/9723477?sjid=643040824425448523-NC#custom-bidding-support-limitations)  
* [Training your algorithm](https://support.google.com/displayvideo/answer/9723477?sjid=643040824425448523-NC#training-your-custom-algorithm)  
  * [About the status of your algorithm](https://support.google.com/displayvideo/answer/9723477?sjid=643040824425448523-NC#about-the-status)

## How custom bidding works

While there are standard [automated bidding strategies](https://support.google.com/displayvideo/answer/2997422) to help you maximize campaign performance, you can use custom bidding if you need advanced control over your bidding strategy that goes beyond what automatic bidding can do.

Custom bidding lets you create a bidding strategy that automatically bids based on which impressions are most important to you.

There are 2 ways you can get started creating your custom bidding algorithm.

* [Use rules to create custom bidding algorithms](https://support.google.com/displayvideo/answer/11118987): Define custom bidding goals to optimize impression values using simple weighted conversions without having to write a script. Rules let you assign value to impressions to build a custom bidding algorithm for your campaign goals.  
* [Write a custom bidding script](https://support.google.com/displayvideo/answer/9728993): Use basic knowledge of python to create custom bidding scripts that let you use first-party data to optimize impression values using non-conversion based goals, such as Brand Lift measurements.

Note: You can also use the [Display & Video 360 API](https://developers.google.com/display-video/api/guides/managing-line-items/custom-bidding) to upload, verify individual custom bidding scripts, and assign custom bidding algorithms to campaigns.

You have granular control over your custom bidding algorithm:

* You can use weighted values to assign higher values to impressions that are more likely to help you achieve your campaign goals and lower values to less relevant impressions.  
* You can use Floodlight tags, custom variables, Google Analytics events, or impression signals to optimize toward specific conversion events.

Your custom bidding algorithm goes through a training phase and uses machine learning to learn from your past campaigns so it can better score and prioritize your bids on the right impressions for your campaign.

### Best practices for conversion tracking with custom bidding algorithms

When including conversions in a custom bid strategy, follow these best practices to ensure the best possible performance:

* Custom bidding with rules: Any insertion order or line item using the algorithm will automatically track that conversion. Reports will display the sum of all tracked by default. Include the Floodlight dimension in your reporting for a more specific view.  
  * When conversions are automatically tracked by the algorithm, the conversions cannot be removed and the lookback window will remain editable.  
    * If the conversions are tracked before the rule based algorithm was assigned, the lookback window remains the same.  
    * If the conversion was added as a result of the algorithm being assigned, the lookback window will be set to default of 90 days which is editable.  
    * Assignment of tracked conversions cannot be edited while the conversions are used by the algorithm and the algorithm is assigned to an insertion order or line item.  
  * The conversion counting will match the type of conversion scoring used in the algorithm. If only post-click conversions are used, the tracked conversion counting will be "Post click only". If post-view conversions are considered in the algorithm, then tracked conversion counting will include "All Conversions".  
* Custom bidding scripts: Ensure all line items that use the script as a bidding strategy also include the conversion under the tracked conversion setting.

### Examples

Custom bidding algorithms can be simple or they can be complex. Here are a few examples of what you can optimize toward:

* Brand key performance Indicators (KPIs): Such as viewability and video completions.  
* Conversion activities: Prioritize toward specific conversion activities by assigning more value to activities that are more relevant to your campaign goals.  
* Custom Floodlight variables: Such as loyalty, products, and basket size.  
* Floodlight Sales revenue: By tracking the revenue parameter using the Floodlight Sales tag.  
* Weighted conversions: Use Floodlight tracking activities that carry specific values to you depending on the product page visited.

* Google Analytics 4: You can link Google Analytics to Display & Video 360 to define weights to events on an advertiser’s site.

Example: Brand optimization with custom bidding  
Example: Maximizing performance for conversion activity  
Example: Maximizing for return on ad spend with Google Analytics and custom bidding

### Summary insights

The custom bidding summary view shows how your impressions have been scored, displaying the distribution of impression scores in a chart. This can help you to better understand the effectiveness of your custom bidding algorithms.

To access summary insights:

1. Open an advertiser or partner.  
2. Click Resources in the left menu, then select Custom bidding.  
3. Select an algorithm, then click the Summary tab.

You can change the time period view of your “Summary” tab from the last 30 days to week over week. This will update the charts to provide insights on how the data has changed compared to the previous week.

The top 3 charts will show data for the past 7 days and provide a comparison to the previous 7 days. The score distribution chart will show the chart of the current past 7 days and then overlay black horizontal lines that represent the previous 7 days allowing you to quickly compare the changes week over week.

Note: The chart will show groupings of values for easier analysis when there are more than 10 distinct values.

## Permission and access

Before you begin, check that you've the permission and access you need.

For algorithms created at the advertiser level:

* You need partner level access or the specific advertiser level access to edit the algorithm.  
* You can’t share the algorithm with other advertisers.

For algorithms created at the partner level:

* You need partner level access to edit the algorithm.  
* You can share the algorithm with multiple partners.  
* You can view the algorithm with advertiser level access, but can’t view which advertisers the algorithm is shared with.

## Custom bidding support limitations

Custom bidding isn't available on YouTube, Programmatic Guaranteed, and Demand Gen inventory.

## Training your algorithm

Your custom bidding model requires a minimum amount of impression data to learn so that it can perform well. Here are the minimum data requirements you must have for each advertiser and individual line item:

|   | Custom bidding goals | Custom bidding scripts |
| :---- | :---- | :---- |
| Minimum data requirements for each advertiser | At least 10,000 scored impressions and a minimum of 500 positively scored impressions | A minimum of 500 positively scored impressions |
| Minimum data requirements for each line item | At least: 50 positively scored impressions Individual impression values must be greater than zero, and in the range of 0.000001 and 1,000,000. Google Analytics goals require clicks. Make sure that there's enough data to generate a model. | At least 50 positively scored impressions |

### About the status of your custom bidding algorithm

Before you can use your custom bidding strategy on an active campaign, you’ll need to check the status of your custom bidding model to make sure it’s ready. Editing or updating your algorithm may change the status of your custom bidding model, so you’ll want to check the state of your model occasionally.

The following describes the state your custom bidding model could be in and what it means:

| Status | What you need to know |
| :---- | :---- |
| Training | Your model is still learning and needs time to learn. What you need to know: Assigning an untrained model to a live campaign will cause your line item to stop spending. You may want to give your algorithm time to learn before you test its performance. As more data becomes available, it improves the accuracy of your results. |
| Insufficient data | Your model doesn’t have the minimum data it needs to learn. What you need to know: Custom bidding uses impression data from the last 30 days, which means: You may have to wait several days before you meet the minimum data requirements If you pause custom bidding for more than 30 days, you may need to wait until you've met the data requirements to train your custom bidding algorithm. Your model may take 1-3 days to train after you have the minimum [data requirements](https://support.google.com/displayvideo/answer/9723477). You can try the following: Edit your algorithm’s scoring criteria or Increase the impression volume to get sufficient data to train your model. |
| Ready | Your model is trained and ready to use. What you need to know: Make sure to assign your model to an active line item to prevent suspension. |
| Suspended | A suspended model stops training using new data. What you need to know: If no spend is associated with a model for 21 days, it gets suspended. This is to prevent unused models from taking up resources. If you need to use a suspended model, you can reactivate it by assigning your model to an active line item or insertion order set up with future budgets or flights within 21 days. |
| Active | Your model is assigned to an active campaign. It’s continuously optimizing and actively bidding. What you need to know: It’s important to continuously monitor how it performs and adjust your algorithm to help improve or maintain its performance. |

# Create and use a custom bidding script

## Create your script

Note:

* If you have partner-level access: You can create the script at either the partner or advertiser level, allowing the algorithm to be shared with multiple advertisers.  
* If you only have advertiser access: You can only create scripts at the advertiser level. The corresponding algorithm will only be associated with the advertiser it's created in.  
1. Navigate to your Partner or Advertiser.  
2. Expand Resources ![and then][image1] Custom Bidding in the left menu.  
3. Choose New Algorithm.  
4. Enter a name for your custom bid.  
5. Select your objective. The objective you choose determines which rules can be selected. Choose Custom then select Use script to define which impressions are most valuable for your campaign.

![new script window][image2]

### Best practices for conversion tracking with custom bidding algorithms

When including conversions in a custom bid strategy, follow these best practices to ensure the best possible performance:

* Custom bidding with rules: Any insertion order or line item using the algorithm will automatically track that conversion. Reports will display the sum of all tracked by default. Include the Floodlight dimension in your reporting for a more specific view.  
  * When conversions are automatically tracked by the algorithm, the conversions cannot be removed and the lookback window will remain editable.  
    * If the conversions are tracked before the rule based algorithm was assigned, the lookback window remains the same.  
    * If the conversion was added as a result of the algorithm being assigned, the lookback window will be set to default of 90 days which is editable.  
    * Assignment of tracked conversions cannot be edited while the conversions are used by the algorithm and the algorithm is assigned to an insertion order or line item.  
  * The conversion counting will match the type of conversion scoring used in the algorithm. If only post-click conversions are used, the tracked conversion counting will be "Post click only". If post-view conversions are considered in the algorithm, then tracked conversion counting will include "All Conversions".  
* Custom bidding scripts: Ensure all line items that use the script as a bidding strategy also include the conversion under the tracked conversion setting.

### Write your script

To learn more about custom bidding script syntax and for samples, go to [Custom bidding script reference](https://support.google.com/displayvideo/answer/11967043).

You can search for linked attributes when writing a custom bidding script:

1. In the New script window, expand Script tools.  
   Note If you're creating your script at the partner level, next Choose an advertiser.  
2. Choose one of the following categories:  
   * Attribution models  
   * Floodlight activities  
   * U-Variables  
3. (Optional) Use the search bar to search for a specific attribute.  
4. Select the copy and paste icon next to the attribute.  
5. Paste the metadata to your script.  
6. (Optional) Select Check syntax to review syntax issues with your script.

### Test your script

Before you create your custom bidding script, you can test your algorithm to generate a chart that shows the distribution of scores for your chosen impressions. You can use this data to test your script's performance and check if it performs as expected.

Sample scenario

To test your script:

1. From the drop-down menu, choose an advertiser.  
   * You must link an advertiser to the algorithm to see them in the list.  
   * The advertiser must meet [custom bidding data requirements](https://support.google.com/displayvideo/answer/9723477).  
2. Under Sample type, choose how impressions are sampled:  
   * All impressions: Recommended to understand overall expected distribution of impression values.  
   * Only impressions with clicks: Useful if clicks are central to the script.  
   * Only impressions with conversions: Useful if conversions central to the script. This sample includes all conversion events in your advertiser and will be based off the default attribution model

You can test your algorithm using a random sample of 10 000 impressions from eligible impressions. You can review the following results:

* The number of impressions in the sample: The number of sampled impressions included in the results.  
* Impression value/cost: The impression value/cost for the sampled impressions.  
  Note: Included in the results only when using all impressions as the sample type.  
* Percentage of execution errors: The percentage of sampled impressions that returned an error after testing the script.  
* Percentage impressions scored: The percentage of sampled impressions successfully scored.  
* Percentage of positive impressions scored: The percentage of sampled impressions successfully scored with a score over 0\.

You can download a .csv file to view the details of individual values in the results.

When you're done, choose Create.

After you create your script, it requires time to process. It may take 20 mins before it's available. When it's available, you can view your script from the script list.

## Get started with a campaign

Your algorithm may take 1–3 days to train after you have saved a script that meets the [data requirements](https://support.google.com/displayvideo/answer/9723477). Once your model is ready, you will see Yes next to Is the model ready? in the model's Summary tab.

1. (Recommended) Set up an [A/B experiment](https://support.google.com/displayvideo/answer/9040669). Your custom bidding algorithm can be the experiment that you test against a control. If your custom bidding model isn't ready yet, you can use a placeholder bid strategy and come back later to update.  
2. In the Insertion Order Details tab for each of your custom bidding test insertion orders, you can select: Optimization ![and then][image3] Automate bid & budget at insertion order level ![and then][image4]Maximize custom value / cost![and then][image5]​​ \[your custom bidding algorithm\]  
   * The system will automatically adjust the insertion order's bids for the highest impression value (determined by your algorithm). Spending your full budget will be prioritized.  
3. Alternatively, In the Line Item Details tab for each of your custom bidding test line items, you can select: Bid strategy ![and then][image6] Automated Bidding ![and then][image7]Maximize custom value / cost![and then][image8]​​ \[your custom bidding algorithm\]  
   * The system can automatically adjust your line item's bids for:  
     1. The highest impression value (determined by your algorithm). Spending your full budget will be prioritized.  
     2. A target value or cost that you set.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAASElEQVR4XmNgGAWDF5SUlCwoLS2djy5OFgAalADE/0EYXY4sgGQg1V1INQPB3qXYQJjLQBGCLkcSoLpBVIlNkGEUu2gU0A8AAEqlM86eADT4AAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,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iYBDnBFwAIBIIuAQZwQcACCSFHClpaUMRiwHAQcAiCQFXCqVYjBiOQg4AEAkcQgVcUbAAQAiiYBDnBFwAIBIIuAQZwQcACCSCDjEGQEHAIgkAg5xRsABACKJgEOcEXAAgEgi4BBnBBwAIJIIOMQZAQcAiCQCDnFGwAEAIomAQ5wRcACASLoaAk77xZqamjNO0z6ztrb2jNOA5kbAAQAiqSkB16tXL/9aVlZm06dPt7pE/X5s185dtmzZMqusrPSfJ06caIWFhQ2XS1dSUmKjRo1KP9n27Nljw4YNO+O0559/3mbOnHnGaYi37du3+/9f2pwIOABAJDUl4P75r3/6V8XZkCFDrLbmh5mxtm3bWlZWls+WPfbYY5ZMJn25ESNG2NatW32Zr7/+2mbPnm25B3Jt5cqVvh/MycnxZXT9CrgePXp4HM6ZM8fXEQZcVVWVjR8/3hYvXuw77+rqahs3blzDz4iP+++/3+bPn9+sv3cCDgAQST824B5++GFbsGCB79+eeuopKyoqsnfeecdef/11u++++3xne/3119stt9xia9eutddee8127dplDz30kL300ku+rALuN7/5jZ/261//2tcRBpyC7+9//7tfXvtRhdvjjz9ud999t1VUVDRsB659S5YssbvuussfB82FgAMARNLlBNzOnTvtgQcesE2bNtnYsWOtXbt2NnXqVFuzdo2/l03nK8xuuukmKy4utldeecWvJz8/3wNOh2KXLl1qb731lrVu3doDTutV7GVmZtq6desaAk5R2KdPH+vYsaMdOHDAFi5c6LN+uu5EIpG2pbjW6RC8Ho8bN25MP+uyEHAAgEhqSsC1bNnSD2VmZ2f7zJr2YzqUqUOd5eXlHmKaidNhVM2u3XbbbT6L9uCDD/rXV1991fLy8hoCLgwyBWH79u094PQ+O11+1qxZ/l6nMOB02f379/t26r12M2bM8J/79u3roYj42Lx5sx9G1eNIj73mQMABACKpKQG3ZcsW69atm7333ns2d+7c9LN9HRMmTPDvFXSajXvjjTesa9euHmmjx4z2r5qN04xdbm6uDRw40NepmDt27Jj179/fevbsad27d/c4HD58uK1fv97DT8vpdO1HNQv37rvv+uUUlYiPVq1aebw1JwIOABBJTQk44GrwU/QTAQcAiCQCDnFGwAEAIomAQ5wRcACASCLgEGcE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>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAASElEQVR4XmNgGAWDF5SUlCwoLS2djy5OFgAalADE/0EYXY4sgGQg1V1INQPB3qXYQJjLQBGCLkcSoLpBVIlNkGEUu2gU0A8AAEqlM86eADT4AAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAASElEQVR4XmNgGAWDF5SUlCwoLS2djy5OFgAalADE/0EYXY4sgGQg1V1INQPB3qXYQJjLQBGCLkcSoLpBVIlNkGEUu2gU0A8AAEqlM86eADT4AAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAASElEQVR4XmNgGAWDF5SUlCwoLS2djy5OFgAalADE/0EYXY4sgGQg1V1INQPB3qXYQJjLQBGCLkcSoLpBVIlNkGEUu2gU0A8AAEqlM86eADT4AAAAAElFTkSuQmCC>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAASElEQVR4XmNgGAWDF5SUlCwoLS2djy5OFgAalADE/0EYXY4sgGQg1V1INQPB3qXYQJjLQBGCLkcSoLpBVIlNkGEUu2gU0A8AAEqlM86eADT4AAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAASElEQVR4XmNgGAWDF5SUlCwoLS2djy5OFgAalADE/0EYXY4sgGQg1V1INQPB3qXYQJjLQBGCLkcSoLpBVIlNkGEUu2gU0A8AAEqlM86eADT4AAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAASElEQVR4XmNgGAWDF5SUlCwoLS2djy5OFgAalADE/0EYXY4sgGQg1V1INQPB3qXYQJjLQBGCLkcSoLpBVIlNkGEUu2gU0A8AAEqlM86eADT4AAAAAElFTkSuQmCC>