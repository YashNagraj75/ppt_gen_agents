Planner_Prompt = """
You are a presentation planning expert. Your job is to determine the best slide layout based on the provided content and available templates. 
Consider both the aesthetic and logical flow for an engaging presentation.
Your task is to propose the most suitable combination of slide layout which adheres to both asthetic and engaging presentation flow for the user.

As you form your suggestion, work through the reasoning step by step:
1) Content Analysis: Start out by analyzing the content  . Start by summarizing the key information from the content. Identify main messages, data points, or visual elements like images ,charts or tables that stand out. 

2) Template Assessment: Evaluate the given slide templates {templates} which contains description and schema of how each template is being used and also some tips for selecting the layout,you will also be given visual representation of the templates via images of the templates which will help you to acess the template more visually, use this information to describe why certain templates might match the identified content elements based on structure (like text hierarchy, image placements, or chart areas).

3) Layout Proposal: At last suggest the presentation (list of slide layout names and title only), considering both aesthetic aspects and functional clarity. Justify your  suggestions as to why you chose that layout. 

While layout proposal give the  layout name in json format with just the title filled for each layout and leave the other 
fields like content empty for now it will be filled later, for the chart just give the type of the chart properly according to the schema.

Therefore the output format is as follows:
1) layout: The layout name strictly according to the layout schema provided
2) title: The title for that layout suggested by you
"""

Text_Prompt = """
You are a slide content generator who has been given the task to generate content for a slide.
You are going to generate content for a given slide with the specified title from the context given to you.
Here are some things you need to keep in mind while generating the content:
1) Format: Generate the content in **PLAIN TEXT** only and no markdown allowed.
2) Content



"""

Layout_Desc = """
Layout 1: titleSlide
Description: This is the titleSlide where the title of the section will be best fit.
Word count: The max word count here would be from 5 to 10 words.
Tips: If you come across a situation where the title is more than this word limit then change the title to fit this word limit while keeping the 
meaning of the title intact
Schema: 
(
  layout: "titleSlide", 
  title: "Sample Presentation",
  subtitle: "Created with pptxgenjs"
)

Layout 2: titleContentSlide
Description: This is the titleContentSlide where the we have a title for the slide and a bullet points for showing 
any important points of the topic.
No of bullet points: A good amount of bullet points here will be from 6 to 10 bullet points.
Tips: If you have content that exceeds these number of bullet points then try to combine them into these number of points or recommend another slide layout that we can take these number of bullet points, but don't cut down on important points from the context
Schema:
(
  layout: "titleContentSlide",
  title: "Available Themes",
  content: "This presentation is using the 'corporate' theme. Other available themes:",
  bulletPoints: [
    "default - Clean and simple design with standard colors",
    "modern - Contemporary look with blue accent colors",
    "corporate - Professional style with dark blue and gold",
    "vivid - Bold, high-contrast design with bright colors"
  ]
)

Layout 3: mediaLeftTextRight
Description: This is the mediaLeftTextRight where the we have a media placeholder on the left and a text placeholder on the right. 
This layout is a perfect visual representation of the text presented on the right.
Word count: The max word count here would be from 100 to 150 words.
Schema:
(
  layout: "mediaLeftTextRight",
  title: "Image Slide",
  content: "This slide demonstrates how to add images to your presentation.",
  image: {
    path: "https://picsum.photos/600/400"
  }
)

Layout 4: mediaSlide
Description: This slide is to display any youtube video that will explain the topic of the subject properly.
Schema:
(
  layout: "mediaSlide",
  title: "Media Slide",
  content: "Caption for the media like Youtube video name or something",
  media: {
    type: 'online',
    link: 'https://www.youtube.com/embed/dQw4w9WgXcQ'
  }
)


Layout 5: tableSlide
Description: This is the tableSlide where the we have a table to represent data points or summary of tables from the content if any
No of rows and columns: A good amount is like 3 columns and 4 rows.
Schema:
(
  layout: "tableSlide",
  title: "Simple Table",
  content: "Placeholder for the what the table describes",
  table: {
    rows: [
      ["Name", "Department", "Sales ($)"], 
      ["John Smith", "Marketing", "125,000"],
      ["Jane Doe", "Engineering", "135,000"],
      ["David Wilson", "Sales", "145,000"]
    ],
  }
)


Layout 6: barSlide
Description: This is the barSlide bar chart which can be used to display trends over or any types of data points available from the context
Schema:
(
  layout: "barSlide",
  title: "Bar Chart (Vertical)",
  content: "Placeholder for description of the bar chart",
  chart: {
    type: "bar",
    data: [
      {
        name: "2023",
        labels: ["Q1", "Q2", "Q3", "Q4"],
        values: [26, 53, 80, 75]
      },
      {
        name: "2024",
        labels: ["Q1", "Q2", "Q3", "Q4"],
        values: [43.5, 70.3, 90.1, 80.05]
      }
    ]
  }
)
"""
Layout_Schema = """
layouts = {
  theme: " corporate", 
  slides: [
    {
      layout: "titleSlide", 
      title: "Sample Presentation",
      subtitle: "Created with pptxgenjs"
    },
    {
      layout: "titleContentSlide",
      title: "Available Themes",
      content: "This presentation is using the 'corporate' theme. Other available themes:",
      bulletPoints: [
        "default - Clean and simple design with standard colors",
        "modern - Contemporary look with blue accent colors",
        "corporate - Professional style with dark blue and gold",
        "vivid - Bold, high-contrast design with bright colors"
      ]
    },
    {
      layout: "mediaLeftTextRight",
      title: "Image Slide",
      content: "This slide demonstrates how to add images to your presentation.",
      image: {
        path: "https://picsum.photos/600/400"
      }
    },
    {
      layout: "mediaSlide",
      title: "Media Slide",
      content: "This slide demonstrates how to add media to your presentation.",
      media: {
        type: 'online',
        link: 'https://www.youtube.com/embed/dQw4w9WgXcQ'
      }
    },
    {
      layout: "tableSlide",
      title: "Simple Table",
      content: "This slide demonstrates how to add a table with data.",
      table: {
        rows: [
          ["Name", "Department", "Sales ($)"], 
          ["John Smith", "Marketing", "125,000"],
          ["Jane Doe", "Engineering", "135,000"],
          ["David Wilson", "Sales", "145,000"]
        ],
      }
    },
    {
      layout: "barSlide",
      title: "Bar Chart (Vertical)",
      content: "Standard vertical column chart with multiple series.",
      chart: {
        type: "bar",
        data: [
          {
            name: "2023",
            labels: ["Q1", "Q2", "Q3", "Q4"],
            values: [26, 53, 80, 75]
          },
          {
            name: "2024",
            labels: ["Q1", "Q2", "Q3", "Q4"],
            values: [43.5, 70.3, 90.1, 80.05]
          }
        ]
      }
    }
}

"""

Content = """
Climate change is one of the most pressing issues of our time, and its impact on biodiversity is profound and far-reaching. As global temperatures rise, ecosystems are being altered, species are facing extinction, and the delicate balance of nature is being disrupted.

The effects of climate change on biodiversity are evident in various ways. For instance, many species are experiencing shifts in their habitats as they attempt to adapt to changing temperatures and weather patterns. This can lead to mismatches in the timing of life cycle events, such as flowering and pollination, which can have cascading effects on entire ecosystems.
"""
