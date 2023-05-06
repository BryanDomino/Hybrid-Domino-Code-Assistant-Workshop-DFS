# Domino Nexus - Hybrid Workshop
An introductory workshop to [Domino Nexus](https://www.dominodatalab.com/nexus) a single pane of glass that lets you run data science and machine learning workloads across any compute cluster — in any cloud, region, or on-premises. It unifies data science silos across the enterprise, so you have one place to build, deploy, and monitor models.

We will also cover some of the basics of Domino's low code assistant [Domino's Code Assistant](https://dominodatalab.github.io/domino-code-assist-docs/latest/)

### Data Source

[Balancing Mechanism Reporting Service](https://www.bmreports.com/bmrs/?q=help/about-us) is the primary channel for providing operational data relating to the GB Electricity Balancing and Settlement arrangements. It is used extensively by market participants to help make trading decisions and understanding market dynamics and acts as a prompt reporting platform as well as a means of accessing historic data.

### Hybrid Multi-Cloud

Our organisation is multi-national with investments in several cloud technologies to support our teams around the world working on different energy production mechanisms. As such our data science teams must navigate data residency rules and process certain types of data in their countries of origin. This can be a very manual task that often involves setting up different technology stacks in the different clouds/regions.

Luckily Domino makes working with remote data trivial through [Domino Nexus](https://www.dominodatalab.com/nexus)!

In this scenario we have our energy production data stored as follows:
* NPSHYD (Non-Pump Storage Hydro) data is in AWS in the west coast of the USA - our main data science hub.
* CCGT (Combined Cycle Gas Turbine) data is in AWS in Dublin, Ireland
* WIND (Wind turbine) data is in Azure in Canada

TODO architecture diagram.

### Domino Code Assistant (DCA)

To make things easier we are going to leverage Domino Code Assist (DCA) a low code assistant for Jupyter/RStudio than can help users learn R/Python, or provide a productivity tool to experienced coders.

#### In this workshop you will work through an end-to-end workflow to ingest, vizualize the remote data as well as build a simple predictive model:

* Set up your Project and add the data in different cloud regions
* Explore data ingest with Code Assist
* Work through pre-built transforms to your data
* Create plots using pre-built visualizations
* Train our forecasting model in the remote cloud
* Assess the performance of the model
* Tune some parameters of our model in batch
* Configure our model to be run on a scheduled basis

## Section 1 - Setting Up Your Project

### 1.1 Fork The Workshop Project

Click on the magnifying glass search icon in the top left of the UI. Search for the "hybrid-workshop" project and click on it when it comes up.

TODO image

To fork the project by clicking the button in the top right of the project overview page:

<p align="center">
<img src = readme_images/fork.png>
</p>

Name your project hybrid-workshop with your initials at the end, e.g. "hybrid-workshop-BJP"

### 1.2 Add The Data to the Project

Domino has many different ways to connect to data but in this example our data is stored in mounted drives in our three different regions, AWS USA West, AWS Ireland and Azure Canada. We will also add a connection to our Snowflake instance that our admin has configured for us, this will be used to consolodate some simple metadata from the different regions.

To add data mounts to our project we need to:

1) Click on "Data" under the Materials section of our project
2) Click on "External Volumes" in the bar along the top
3) Click on the "Add External Volume" button and select on of the volumes
4) Repeat 3) until all the volumes have been added to your project

<p align="center">
<img src = readme_images/data_volumes.png width="800">
</p>

To add the Snowflake data source to our project we need to:

1) Click on "Data" under the Materials section of our project
2) Click on "Data Sources" in the bar along the top
3) Click on the "Add Data Source" button
4) Only one data source is available, our Snowflake instance, configured with it's service account credentials. Click **add to project**.

<p align="center">
<img src = readme_images/data_sources.png width="800">
</p>

### 1.3 Creating a Workspace

Workspaces in Domino are the interactive development environments. 

To start one navigate to the Workspaces tab on the left, and select “Create New Workspace”.

<p align="center">
<img src = readme_images/create_workspace.png width="800">
</p>

Domino is an open platform that supports many different IDEs, giving data scientists the flexability to work with the tools they are most productive with. In this example we will use JupyterLab so select that.

Next we need to decide which cloud and which region we want to work on. **Domino makes this really easy.** Click on the Hardware Tier drop down. You will be provided with a list of different hardware that you can run your work on. Select one of the Small instances in 'Local' (AWS USA West), AWS Ireland or Azure Canada depending on which data you would like to work with:

* NPSHYD (Non-Pump Storage Hydro) data is in AWS in the west coast of the USA - our main data science hub.
* CCGT (Combined Cycle Gas Turbine) data is in AWS in Ireland
* WIND (Wind turbine) data is in Azure in Canada


<p align="center">
<img src = readme_images/hardware_tier.png width="800">
</p>

Next click on **Compute Cluster**. Domino also gives us the flexability to create distributed compute clusters in the different clouds without the devops overhead! So if we wanted to use a Spark cluster for our data preparation, or a Ray cluster for distributed model training or even MPI on our on-premise HPC hardware we can do that at the click of a button.

<p align="center">
<img src = readme_images/clusters.png width="800">
</p>

Navigate to the additional details settings. Note that you can see which data volumes are available in the region you have selected. You will not be able to access the data in the other regions in this case, maintaining our data residency.

<p align="center">
<img src = readme_images/edv_details.png width="800">
</p>

Click on the Launch button to start your workspace. This may take several minutes to start as it is seamlessly provisioning resources for you in a distant cloud no devops work or IT tickets required!

This demonstrates how Domino removes the complexity of hybrid and multi-cloud environments by providing a single seamless interface for working in different geographies/clouds with different data.


### 1.4 Initializing DCA in a Notebook: Python

Once your IDE is started up, create a new Notebook and rename it "Hybrid_Tutorial.ipynb"

<p align="center">
<img src = readme_images/new_workspace.png width="800">
</p>

Then click on the blue **Domino Code Assist** button on the toolbar to initialize the Code Assistant. 

<p align="center">
<img src = readme_images/DCA_init.png width="800">
</p>

When you hover over the next cell in your Notebook, a blue DCA icon should appear on the left. This is where we’ll access the DCA tools.

<p align="center">
<img src = readme_images/DCA-icon.png width="800">
</p>

## Section 2 - Data Ingest

There are many ways to load a dataset into your notebook using Code Assist. To get started, in the DCA Menu, select Load Data from the DCA menu:

<p align="center">
<img src = readme_images/DCA_menu_load_data.png width="800">
</p>

* **Data Sources** Domino Data Sources allow you to browse [Domino Data Sources](https://docs.dominodatalab.com/en/latest/user_guide/fbb41f/data-sources/) that have been added to your Project. These could include cloud data stores like S3 buckets, ADLS, BigQuery, Snowflake etc., on-prem data sources such as an Oracle Database, or Trino's distributed query engine. Domino Data sources are accessed at the user level, and read/write credentials are stored in your user account when the connector is set up in a Project.

* **Datasets:** Domino Datasets are network file systems managed by Domino that can be snapshotted for reproducibility, and shared amongst users and / or projects. Domino Datasets are typically used for files that are too large to save in the project file system. 

* **Project Files:** Project files are typically used for code, visuals, notebooks and smaller datasets (<10GB). These files are continuously versioned each time you sync your workspace. 

* **Upload:** DCA uploads support drag-and-drop uploads local files from your machine such as CSV files or local directories. 

* **Quick Start:** has some demo datasets for testing playing around with DCA.

For this tutorial, we’ll want to access the dataset in the project files that has been mounted into the `data` folder. 
Select the "data.csv" file. For simplicity the location and filename will be the same regardless of which region you chose.
Note at the bottom that it saves this dataset as `df`.
Click **Run** to load the data into the pandas dataframe. Note that the code is generated for you!

<p align="center">
<img src = readme_images/load_data.png width="800">
</p>

## Section 3 - Data Transformations

You’ll notice most observations are at a 30-minute interval, but we’ve got some entries at odd intervals that have missing values from some sources. We can filter out null values using the DCA’s Transformations feature.

In a new cell in your notebook, mouse over the DCA icon on the right and select **Transformations**. If you mouse over individual cells, you’ll see a popup appear next to the cell that allows you to **Filter values like this**. Hover over the `NaN` value in the "Other" column, and select the filter:

<p align="center">
<img src = readme_images/filer_nan.png width="800">
</p>

Then, change the filter to **!=** NaN, and click **Apply**.

<p align="center">
<img src = readme_images/filter_nan_not_equal.png width="800">
</p>

If you scroll down to the bottom and toggle on **Show Code**, you can see the sample code that DCA has written. While you can always come back and edit this code, either manually or in the code assistant window, the preview is a handy feature for examining the sample code before inserting it into your notebook.

<p align="center">
<img src = readme_images/show_code.png width="800">
</p>

As a final step, go ahead and filter out the null values in the CCGT/WIND/NPSHYD column in the spreadsheet, depending on which data you are working with. After applying the new transform, the following code (or similar) should appear in the preview:

```
df = df.loc[df["OTHER"].notna()]
df = df.loc[df["CCGT"].notna()]
df
```

Go ahead and click **Run** to insert the filtered null values.

You may be wondering if this method is inefficient for applying filters to really wide datasets with 100s columns - why not just use a method like `df.dropna()`? The answer is that you _should_ use features beyond what is offered out of the box with DCA. Code assist is just meant to be a starter, but you should feel free to build on features here and not be limited by the assistant. In fact, you can save commonly used code as custom snippets, which we’ll cover later. 

## Section 4 - Visualizations

After cleaning up our data, the next step is to visualize it. 

From the DCA menu, select **Visualizations**.

Select the data frame name you in the previous steps ('df'), and set the plot type to **Area**.

Set the X-axis to “datetime” and the Y-axis to “CCGT”, "WIND" or "NPSHYD" depending on which data you are working with.

Under Options, set the Theme to any you like.

Inspect the code at the bottom, then hit **Run**

<p align="center">
<img src = readme_images/area_plot.png width="800">
</p>

You now have an Area chart of power generated by your selected source. Note that this is just one of many types of plots, and you can customize the plot from here - feel free to modify the Python (or R) code DCA has written for you.

## Section 5 - Training our Model using Code Snippets

So far, we have relied on DCA’s existing features to apply transforms or plot our data. But what if we want to do something DCA doesn’t do out of the box? For example, what if we want to do time-based aggregations, or plot electric production by source all on a single area plot?

For these types of custom tasks, Domino Code Assist has code snippets. 

### 5.1 Saving Snippets to a Project

First, remember back to when we removed rows with null values. If we had many columns, rather than selecting null values in columns one by one, we could use the following pandas code. This drops any row that contains at least one null value in any column:

```
df = df.dropna(axis=0, how='any')
df
```

Copy the code above into the next empty cell. In the DCA menu, next to the last line **Insert Snippet**, click on the pencil icon to enable editing snippets. This allows you to add new code snippets to the code snippet library. 

<p align="center">
<img src = readme_images/enable_snippet.png width="800">
</p>

Click on **Save as Snippet**:

<p align="center">
<img src = readme_images/save_snippet.png width="800">
</p>

Give your snippet the name `drop_null_rows`, select the current project as your repository, and click **Add**.

This is great, but currently these snippets are only available in the current project files. What if I want to make a snippet available to everyone in other Projects, or even other instances of Domino? 

There are two ways to save code snippets:

1) As files in your project in the snippets folder.
2) Saved to an external repository that has been added as an **Imported Code Repository** to the project using the git service of your choice (Github, Gitlab etc.)


### 5.2 Training our model using Snippets

Now that we have our base data and we've removed any missing values we want to use this to build a predictive model so we can estimate future demand for our fuel type.

For this we want to create a new data frame that just has the timestamps and the fuel amount. We'll then want to split this out into a training and testing set.

For the predictive modelling we are going to use [Prophet](https://facebook.github.io/prophet/), which is already installed in this environment.

Finally, we will want to save this model in case we wanted to utilise it later in the project as an batch model, API or in a web app for example.

To save time and complexity we have created a code snippet in DCA that we can use to train the model.

To try this out go back to the DCA menu, select **Insert Snippet**, select the following snippet, and click **Run**:

`train_model`

<p align="center">
<img src = readme_images/train_snippet.png width="800">
</p>

This code will train our model. We're not aiming for the worlds greatest forcasting model, this is just an example.


### 5.3 Forecast Fuel Demand

Once we have built our model we want to start forecasting how much CCGT, WIND or NPSHYD fuel we will need in the future. To do this we can leverage Prophet's predict function on our model over a period of time.

We can then plot this out using Matplotlib to see roughly how well our model is performing on this small set of data.

Again, to simplify this step we can use a code snippet in DCA. In a new cell go to the DCS menu, select **Insert Snippet**, select the following snippet, and click **Run**:

`predict_demand`

<p align="center">
<img src = readme_images/demand_snippet.png width="800">
</p>

Note: this will take a couple of minutes to run.

We can see from the graph how well our model is predicting the demand. No doubt this could be improved with a lot more data and some parameter tuning!


### 5.3 Cross Validation

We now want to calculate some performance metrics to assess the quality of the model we have trained. Luckily Prophet has a built in cross validation function that allows us to configure different time windows and calculate our RMSE and MAE.

Again, to simplify this step we can use a code snippet in DCA. In a new cell go to the DCS menu, select **Insert Snippet**, select the following snippet, and click **Run**:

`cross_validation`

<p align="center">
<img src = readme_images/validation_snippet.png width="800">
</p>

Note: this will take 3 or 4 minutes to run, longer if you changed the initial or horizontal parameters. 

At this point we have finished training our model. 

The Snowflake call is sending metadata back to a central app. You can check where you and the other people in the workshop have been running your workloads on the main screen at the front of the class.

Next we will may want to tune the parameters of our model. This can be done using Domino's batch processing mechanism - Jobs. We are finished with our Workspace now, so you can click **Stop** at the top of the workspace to shut down the container and release the resources.


## 6.0 Batch Workloads

What if we wanted to try some different parameter combinations to our model so we can tune it's effectiveness? We could do this in our workspace, and in this example that would be ok because we have a very small dataset. But if our training jobs took hours or even days, we would want to paralellise that. This is where Domino's **Jobs** functionality comes in. It allows us to run multiple simultaneous Jobs. These jobs can be any type of script, so could be used to data preparation, data processing, model training, model inference or any other batch task in your process.

We will also want to schedule this retraining to run on a regular basis as our remote data will be updated regularly by other processes. Domino has a **Scheduled Job** capability for that.  


### 6.1 Domino Jobs 

To get a sense how Domino Jobs work, first take a look at the Python script `pull_daily_data.py` in your project files. This is a script that pulls data from BMRS’s website, using an optional user-specified start and end date. It cleans up the raw data, then appends it to the generation history in the Project’s Domino Dataset.

By default, it pulls the last 24 hours of data. To get a longer history saved to start with, we'll stat by running this script manually.

Navigate out of your workspace, back to the Project, and click on Jobs on your Project's left hand menu. Click on Run, and in the File Name or Command enter the following command. We’ll tell it to pull data from January 1st up to today:

```
pull_daily_data.py '--start=2023-01-01 00:00:00'
```

Ensure your Run Environment matches your Workspace environment, and click on **Start**.

<p align="center">
<img src = readme_images/manual_job.png width="800">
</p>

In the background, Domino is executing our script as a job - it will ping BMRS’s site, download data, clean it up and save it in a Domino Dataset in our Project. This may take a minute, but the status should change from blue to green when the job is complete.

Click into the `pull_daily_data` job run.

In the **Details** tab on the right, note that the compute environment and hardware tier are tracked to document not only who ran the job, but when it was run and what versions of the code, software, and hardware were executed. 

Click into the **Results** tab. Here you can see any data, saved figures, and outputs from the script that was run.

### 6.2 Scheduled Jobs 

If we want to run this every day, we can use Domino to run the Job on a schedule. In the Jobs section of your Project, navigate to the **Schedules** tab, and click **Schedule a Job**.

Call your job `Pull Daily Data`.

Just like with the manual Job, enter the script you want to run. It defaults to pulling the last 24 hours of data, so no need to pass it a start time: 

```
pull_daily_data.py
```
Ensure your Run Environment matches your Workspace environment, and click **Next** until you're in the Schedule tab.

<p align="center">
<img src = readme_images/schedule_1.png width="800">
</p>

Set your Job to run every day at midnight:

<p align="center">
<img src = readme_images/schedule_2.png width="800">
</p>

Click to the last window and Click **Create**. Now the power generation data will be updated every day at midnight.

### 6.TODO Summary

Don't forget to Stop your workspace when you're done, and happy app building!