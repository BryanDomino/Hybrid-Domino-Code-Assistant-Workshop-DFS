# Domino-Code-Assistant-Workshop
An introductory workshop to [Domino's Code Assistant](https://dominodatalab.github.io/domino-code-assist-docs/latest/)

### Data Source

[Balancing Mechanism Reporting Service](https://www.bmreports.com/bmrs/?q=help/about-us) is the primary channel for providing operational data relating to the GB Electricity Balancing and Settlement arrangements. It is used extensively by market participants to help make trading decisions and understanding market dynamics and acts as a prompt reporting platform as well as a means of accessing historic data. 

#### In this workshop you will work through an end-to-end workflow to ingest, clean & vizualize data from BMRS:

* Set up Domino Code Assist in your Project & Workspace
* Explore data ingest with Code Assist
* Work through pre-built transforms to your data
* Create plots using pre-built visualizations
* Insert and create code snippets for future re-use
* Build an app using Domino Code Assistant 

## Section 1 - Setting Up Domino Code Assistant (DCA)

### 1.1 Installing Domino Code Assistant (DCA)

Domino Code Assistant is simply a Python or R package running in a Domino Workspace.

There are four distinct approaches to installing Domino Code Assist (DCA) for either Python or R:

* Install in a Workspace
* Install in a Project
* Install in a Compute Environment
* Install from Source.

The first approach is the easiest way to get started with DCA. But if you restart you workspace, then you will need to reinstall DCA, which is a bit slower. The second and third approaches will enable DCA more permanently.

For this lab, we'll use a Compute Environment  with DCA already installed, which will be a Domino Standard Environment for Domino 5.5 or later. To ensure all workspaces have DCA pre-installed, go into the settings tab in your Project. Ensure the compute environment is set to a Domino 5.5+ standard environment: 

<p align="center">
<img src = readme_images/default_env.png width="800">
</p>

For details on how to install Domino Code Assistant in a Workspace or Project rather than environment, see the [DCA Install Documentation].(https://dominodatalab.github.io/domino-code-assist-docs/latest/install/#install-in-a-workspace)

### 1.2 Initializing DCA in a Notebook: Python

Now that we have a default Project environment with DCA pre-installed, create a new workspace.  

In your Project, navigate to the Workspaces tab on the left, and select “Create New Workspace”. Leave the default Hardware Tier and Environment.

Select the IDE of your choice, and click Launch. Most of the images in this tutorial use JupyterLab, so you may want to select JupyterLab to make it easier to  follow along. However, if you are an R user, feel free to launch RStudio instead to use the R version of DCA.

Once your IDE is started up, craete a new Notebook and rename it "DCA_Tutorial.ipynb"

<p align="center">
<img src = readme_images/new_workspace.png width="800">
</p>

Then click on the blue Domino Code Assist button on the toolbar to initialize the Code Assistant. 

<p align="center">
<img src = readme_images/DCA_init.png width="800">
</p>

When you hover over the next cell in your Notebook, a blue DCA icon should appear on the left. This is where we’ll access the DCA tools.

<p align="center">
<img src = readme_images/DCA-icon.png width="800">
</p>

### 1.2 Initializing DCA in a Notebook: R Studio

DCA works similarly between Python notebooks and R Notebooks, but the UI is different. 

Create a new Workspace, but choose R Studio as your IDE. 

Once R Studio is up and running, there is no need to initialize DCA, the DCA tools are already available in the Addins menu:

<p align="center">
<img src = readme_images/R_Init.png width="800">
</p>

## Section 2 - Data Ingest

There are many ways to load a dataset into your notebook using Code Assist. To get started, in the DCA Menu, select Load Data from the DCA menu ("DCA Load Data" for R Studio Users): 

<p align="center">
<img src = readme_images/DCA_menu_load_data.png width="800">
</p>

* **Data Sources** Domino Data Sources allow you to browse [Domino Data Sources](https://docs.dominodatalab.com/en/latest/user_guide/fbb41f/data-sources/) that have been added to your Project. These could include cloud data stores like S3 buckets, ADLS, BigQuery, Snowflake etc., on-prem data sources such as an Oracle Database, or Trino's distributed query engine. Domino Data sources are accessed at the user level, and read/write credentials are stored in your user account when the connector is set up in a Project.

* **Datasets:** Domino Datasets are network file systems managed by Domino that can be snapshotted for reproducibility, and shared amongst users and / or projects. Domino Datasets are typically used for files that are too large to save in the project file system. 

* **Project Files:** Project files are typically used for code, visuals, notebooks and smaller datasets (<10GB). These files are continuously versioned each time you sync your workspace. 

* **Upload:** DCA uploads support drag-and-drop uploads local files from your machine such as CSV files or local directories. 

* **Quick Start:** has some demo datasets for testing playing around with DCA.

For this tutorial, we’ll start with a small dataset in the project files saved in the `data` folder. Note at the bottom that it saves this dataset as `df` - you may want to change this if you plan to bring in multiple datasets into your notebook.

<p align="center">
<img src = readme_images/load_data.png width="800">
</p>

## Section 3 - Data Transformations

You’ll notice most observations are at a 30-minute interval, but we’ve got some entries at odd intervals that have missing values from some sources. We can filter out null values using the DCA’s Transformations feature.

In a new cell in your notebook, mouse over the DCA icon on the right and select Transformations. If you mouse over individual cells, you’ll see a popup appear next to the cell that allows you to **Filter values like this**. Hover over the `NaN` value in the CCGT column, and select the filter:

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

As a final step, go ahead and filter out the null values in the OTHER column in the spreadsheet. After applying the new transform, the following code should appear in the preview:

```
df = df.loc[df["CCGT"].notna()]
df = df.loc[df["OTHER"].notna()]
df
```

Go ahead and click **Run** to insert the filtered null values.

_Optional: Feel free to load a demo dataset such as Palmer Penguins to test out the other features, such as group-by and aggregate._

You may be wondering if this method is inefficient for applying filters to really wide datasets with 100s columns - why not just use a method like `df.dropna()`? The answer is that you _should_ use features beyond what is offered out of the box with DCA. Code assist is just meant to be a starter, but you should feel free to build on features here and not be limited by the assistant. In fact, you can save commonly used code as custom snippets, which we’ll cover later. 

## Section 4 - Visualizations

After cleaning up our data, the next step is to visualize it. 

From the DCA menu, select **Visualizations**.

Select the data frame name you saved `app_data.csv` to, and set the plot type to **Area**.

Set the X-axis to “datetime” and the Y-axis to “CCGT” (or any column of your choice).

Under Options, set the Theme to any you like.

Inspect the code at the bottonm, then hit **Run**

<p align="center">
<img src = readme_images/area_plot.png width="800">
</p>

You now have an Area chart of power generated by your selected source. Note that this is just one of many types of plots, and you can customize the plot from here - feel free to modify the Python (or R) code DCA has written for you.

## Section 5 - Code Snippets

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

To test it out, create a new Notebook, and repeat the first steps, but with the new snippet:

1) Initialize code assist in the first cell
2) Import `app_data.csv` from Project Files in the second cell
3) In the DCA menu, go to **Insert snippet**, and select your new `drop_null_rows` code to insert in the third cell

<p align="center">
<img src = readme_images/drop_null_example.png width="800">
</p>

Close out of your test notebook, and delete it if you'd like.


### 5.2 Importing an Existing Snippet

What if we wanted to plot production by all sources on the same area plot? We could write a function to stack the dataframe by source, then select a specific time window to plot. DCA doesn't do this out of the box, but fortunately this code already exists from a different project. To prevent repeating work, we could save this “stacking” and time window selection code into a snippet, and make it easily reusable code in other projects.

To try this out, return to your first notebook, and in the DCA menu, select **Insert Snippet**, select the following snippet that was created earlier for this lab, and run it:

`stack_power_by_source`

<p align="center">
<img src = readme_images/import_stack.png width="800">
</p>

This code allows us to build an ares plot of production by all sources over the last day and week. The data frames are saved as `df_today` and `df_week`.

Now, in the next cell, create a plot of power production in the last week by source. From the DCA menu, select **Visualizations**, and fill out the following cells:

* DataFrame: df_week
* Plot Type: Area
* X-axis: datetime
* Y-axis: Production (MW)
* Color: Source

<p align="center">
<img src = readme_images/area_plot_by_source.png width="800">
</p>

Change the theme if you’d like, and **Run** to build your area plot.

Depending on which theme you picked, your plot should look something like this:

<p align="center">
<img src = readme_images/week_plot.png width="800">
</p>

### 5.3 Sharing Snippets with Other Users and Projects

This is great, but currently these snippets are only available in the current project files. What if I want to make a snippet available to everyone in other Projects, or even other instances of Domino? 

There are two ways to save code snippets:

1) As files in your project in the snippets folder.
2) Saved to an external repository that has been added as an **Imported Code Repository** to the project using the git service of your choice (Github, Gitlab etc.)

If you add a public repository, you will have read-only access to snippets, meaning you can pull snippets in, but not save new snippets from your current workspace. If you want to try adding a public, read-only snippets repository, add this Github repository to your Project (no credentials needed):

https://github.com/dominodatalab/low-code-assistant-snippets

In your Project, navigate to the **Code** tab on the left, then the **Git Repositories** tab at the top. Click on **Add a New Repository**. 

Paste the URI above, select **Github** as the Git Service Provider click **Add Repository**.

<p align="center">
<img src = readme_images/add_git_repo.png width="800">
</p>

_Note that once you add an external repository to your Project, you need to create a new Workspace. Sync your current Workspace to the Project, stop it, then create a new Workspace in the Project for the imported repository to be visible to Domino’s Code Assist._

Open up your Tutorial Notebook again, run all cells, then navigate to the DCA **Insert Snippets** menu in a new cell. You'll see an new `python` or `r` folder with the imported snippets now available.



**Optional:** If you'd like to save save your snippets to an external repository, you'll need to add or create a git repository that you have read write permissions for. The steps are: 

1) Save your git credentials in your user account that give you read / write access to the snippets repository. Detailed instructions [here](https://docs.dominodatalab.com/en/latest/user_guide/314004/import-git-repositories/#step-1-create-credentials)
2) Just like with the public repo, import the Git repo as an external repository to your Project and attach your read / write credentials. Detailed instructions [here](https://dominodatalab.github.io/domino-code-assist-docs/latest/project/files/)


This example project has two git repositories for accessing snippets imported into the project. The first is a public repository, has no credentials, and can be used just for importing existing snippets. The second has read / write credentials attached, and can be used for reading, editing and saving new snippets.

<p align="center">
<img src = readme_images/snippet_repos.png width="800">
</p>

Once you have an external snippets repo with read / write permissions added, you'll have the option to save snippets locally or in the external repo when you save them:

<p align="center">
<img src = readme_images/snippets_repo_example.png width="200">
</p>

## 6.0 Building a Live App with Domino Code Assistant

What if we wanted to build an interactive, hosted app that displays power generation live as it comes in from an external source? So far, we have worked with a static dataset, but what if we wanted our power generation plot to refresh on a schedule and display in an app? 

You can accomplish this in Domino using two features: Scheduled Domino Jobs and Hosted Apps. 

Scheduled jobs simply run a Python or R script from your Project in a container. Hosted apps make interactive apps available to other users in your organization via a web browser. You can write an app in any language you like - R Shiny, Flask, Dash, Streamlit and others, or you can use the Domino Code Assistant to turn your notebook into an app.

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


### 6.3 Domino Code Assistant Live App 

Now that we have continuously refreshed data being saved to our Project, we can build an app.

Domino’s Code Assistant can convert the data, plots, widgets and markdown cells in our Notebook into an interactive App automatically. To try it out, navigate to your Workspace and open up the Notebook `DCA_app.ipynb`.

This notebook repeats most of the steps we built previously, except that it reads out of our dataset that is updated each day using the scheduled job we created in Section 6.2.

**Run all cells in the Notebook.**

After running, in the last cell, open up the DCA menu, and select **App**. Toggle on the plots, description and widgets on the left side, and arrange them however you’d like to see them. 

<p align="center">
<img src = readme_images/toggle_on.png width="800">
</p>

Once you’re happy with the arrangement, click Run.

Be sure to toggle on `widget_1`. This is a filter widget that allows the user to select one or more power sources to display in the power generation plot, and is one of the pre-built interactive widgets avaiable from DCA.

DCA’s App builder has written the code for our interactive app. Click on Preview App to see how it would look in a browser window.

If you want to customize the app - add more data, plots - anything you'd like, simply add additional cells to your notebook. Edit your final app cell from the DCA menu, and toggle your new cells on to add them in.

If it looks good, click **Deploy App**, wait a few minutes, and check your app out. 

Navigate back to your Project, and select the App tab on the left. Once your App is ready, click **View App** and play around with it. Note that every time you run (or Domino runs) the `pull_daily_data` job, the source data for this app is updated. By refreshing the browser window, you app will update on live data - no need to restart it, the underlying jobs and app refreshes are now all automated by Domino. 

<p align="center">
<img src = readme_images/view_app.png width="800">
</p>

Don't forget to Stop your workspace when you're done, and happy app building!