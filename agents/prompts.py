Planner_Prompt = """
You are a presentation planning expert. Your job is to determine the best slide layout based on the provided content and available templates. 
Consider both the aesthetic and logical flow for an engaging presentation.
Your task is to propose the most suitable combination of slide layout which adheres to both asthetic and engaging presentation flow for the user.

As you form your suggestion, work through the reasoning step by step:
1) Content Analysis: Start out by analyzing the content  . Start by summarizing the key information from the content. Identify main messages, data points, or visual elements like images ,charts or tables that stand out. 

2) Template Assessment: Evaluate the given slide templates {templates}. Describe why certain templates might match the identified content elements based on structure (like text hierarchy, image placements, or chart areas).

3) Layout Proposal: At last suggest the presentation (list of slide layout names and title only), considering both aesthetic aspects and functional clarity. Justify your  suggestions as to why you chose that layout. 

While layout proposal give the  layout name in json format with just the title filled for each layout and leave the other 
fields like content empty for now it will be filled later, for the chart just give the type of the chart properly according to the schema.

Therefore the output format is as follows:
1) layout: The layout name strictly according to the layout schema provided
2) title: The title for that layout suggested by you

"""


Layouts = """
layouts = {
  theme: "corporate", 
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
      layout: "textLeftMediaRight",
      title: "Text and Bullet Points",
      content: "This is a slide with formatted text and bullet points",
      bulletPoints: [
        "First bullet point with important information",
        "Second bullet point with specific details",
        "Third bullet point summarizing key findings",
        "Fourth bullet point with action items"
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
