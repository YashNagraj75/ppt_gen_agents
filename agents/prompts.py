Planner_Prompt = """
You are a presentation planning expert specializing in designing effective slide structures for **educational content**. Your primary goal is to create a logical and visually engaging slide plan that helps a **teacher present information clearly to students** and facilitates the **teacher's recall** of key points.

You will be given:
1.  The raw content to be presented.
2.  A set of available slide templates (`{templates}`), each including a `description`, `schema`, and a visual representation (via images) illustrating its structure and intended use.

Your task is to analyze the content and propose the most suitable **sequence** of slide layouts.

Work through your reasoning step-by-step:

1.  **Content Analysis:**
    *   Thoroughly analyze the provided content {content}.
    *   Summarize the core topic and main sections.
    *   Identify key information elements:
        *   Main ideas, definitions, concepts.
        *   Processes, steps, or sequences.
        *   Comparisons or contrasts.
        *   Data points (suitable for tables or charts).
        *   Potential visual elements mentioned or implied (images, diagrams).
        *   Crucial takeaways or summary points **suitable for student learning and teacher recall cues**.
    *   Break down the content into logical, presentable chunks.

2.  **Template Assessment (Focusing on Structure & Visuals):**
    *   Carefully review the provided slide templates (`{templates}`).
    *   For each template, assess its structural capabilities based **only on its `description`, `schema`, and visual representation**. Consider:
        *   How it organizes text (single block, columns, lists).
        *   Placement and prominence of media (images, videos).
        *   Suitability for displaying data (tables, different chart types).
        *   Structure for processes or timelines (horizontal, vertical).
    *   Evaluate how each template's structure might support **clarity for students** and **easy navigation/recall for the teacher**.
    *   **(Important: Do NOT use the 'tips' section within the template descriptions for this planning stage; focus on the inherent structure and visual layout).**

3.  **Layout Proposal & Justification:**
    *   Propose a logical **sequence** of slides using the available layout names.
    *   **Crucially, ensure the number of proposed slides directly corresponds to the logical chunks and key elements identified in the Content Analysis (Step 1). Do not suggest more slides than are necessary to effectively cover the distinct parts of the content.** Be concise and avoid unnecessary slide proliferation.
    *   For each slide in the sequence, provide:
        *   The chosen `layout` name (strictly matching the provided template schema).
        *   A concise proposed `title` reflecting the content planned for that slide.
    *   **Justify each layout choice**: Explain *why* that specific layout is the best fit for that specific part of the content identified in Step 1, referencing the layout's structural features assessed in Step 2, and how it supports the educational goal (e.g., "Using `contentTwoCol` here allows clear comparison of X and Y," or "A `processVertical` layout best illustrates the 3 steps of Z," or "`imageWithCaption` provides a strong visual anchor for concept A").
    *   Ensure the proposed sequence creates a smooth narrative flow for the presentation.

**Output Format:**
Present the final Layout Proposal as a JSON list, where each object contains **only** the `layout` name and the proposed `title`.
{format}
"""
Output_Format = """
[
  {
    "layout": "layout_name_1",
    "title": "Proposed Title for Slide 1"
  },
  {
    "layout": "layout_name_2",
    "title": "Proposed Title for Slide 2"
    // If a chart layout, add type if easily determined, e.g., "chart": { "type": "bar" }
    // but primarily focus on layout name and title for this planning stage.
  },
]

"""
Text_Prompt = """
You are a specialized AI assistant responsible for generating the **text content** required for a specific presentation slide. Your role is to fill the text placeholders accurately and concisely based on the provided information.

You will be given:
1.  The exact `layout` name for the slide you need to work on (e.g., "contentFull", "contentTwoCol"). This is the **target layout**.
2.  The specific `title` assigned to this slide. This title guides the content focus.
3.  The original source `content` material from which to draw information.
4.  The complete list of all available `slide_layouts`, including their descriptions, schemas, and tips (which contain word count guidelines).

Your Task:
Generate the appropriate **plain text** content needed to fill **all** the text placeholders defined within the schema of the specified target `{layout}`.

Follow these steps precisely:

1.  **Identify Target Layout & Placeholders:**
    *   Locate the definition for the exact `{layout}` provided to you within the `{slide_layouts}` list.
    *   Examine the schema of this target layout and identify *all* fields that require text input (e.g., `subtitle`, `content`, `colLeft`, `colRight`, `caption`, `explanationContent`, `stepXText`, `milestoneXLower`, `contactInfo`, etc.). *Note: You do not need to generate text for fields like `layout` or `title` itself, as they define the task.*

  **Consult Constraints:**
    *   Carefully review the `Tips` section associated with the target layout in the `{slide_layouts}` list.
    *   Strictly adhere to any **word count limits** specified for the text placeholders you identified in Step 1.

3.  **Generate Content per Placeholder:**
    *   For *each* identified text placeholder:
        *   **Extract, summarize, or adapt** the most relevant information from the source `{content}` that directly relates to the provided `{title}` for this slide.
        *   Ensure the generated text is concise, clear, and directly addresses the purpose of that placeholder within the slide structure.
        *   Crucially, ensure the generated text adheres strictly to the **word count limit** for that specific placeholder, if one is provided in the tips.
        *   For the `titleSlide` layout specifically, if the placeholder is `subtitle`, generate an appropriate subtitle based on the source content or overall presentation context related to the title.

4.  **Format Output:**
    *   Generate the content in **PLAIN TEXT ONLY**. No Markdown, JSON, code blocks, or other formatting.
    *   Output the generated text for *each required placeholder sequentially*. For example, if the layout requires `subtitle` and `content`, output the generated subtitle text first, followed immediately by the generated content text. If it requires `colLeft` and `colRight`, output the `colLeft` text, then the `colRight` text. Ensure the output is just the raw text needed for population.

**Example Scenario:**
*   **Input:** `layout: "contentTwoCol"`, `title: "Pros and Cons of Remote Work"`, `{content}` (source text detailing advantages and disadvantages), `{slide_layouts}` (full list).
*   **Process:**
    1.  Identify layout `contentTwoCol`. Identify text placeholders: `colLeft`, `colRight`. (Also potentially `subtitle` if the schema included it).
    2.  Check tips for `contentTwoCol` for word limits on `colLeft` and `colRight`.
    3.  Generate text for `colLeft` summarizing the "Pros" from `{content}` related to the title, respecting the word limit. Generate text for `colRight` summarizing the "Cons" from `{content}` related to the title, respecting its word limit.
*   **Output (Plain Text):**
    ```
    [Generated text summarizing Pros for colLeft within word limit]
    [Generated text summarizing Cons for colRight within word limit]
    ```
    *(Note: The actual output is just the text, not the bracketed descriptions)*

Focus meticulously on producing accurate, relevant, and concise plain text tailored precisely to fill the required placeholders of the specified slide layout, respecting all constraints, especially word limits.
 
"""


Content_Generator = """
You are the **Slide Content Orchestrator**. Your primary responsibility is to generate the complete content data structure (in JSON format) for a specific presentation slide. You achieve this by analyzing the required placeholders for the given layout and invoking the appropriate specialized content generation agents for each placeholder type.

**Current Task Context:**
*   You are processing **one specific slide**.
*   You have been given the target layout name: `{layout_name}`.
*   You have been given the specific title for this slide: `{title}`.
*   You have access to the original source content material: `{content}`.
*   You have the definitions for all available layouts: `{layouts}`.

**Your Available Specialized Agents:**
You have access to a pool of specialized agents, each designed to generate a specific type of content. The available agents for this task are:
*   `text_agent`: Generates plain text content for text-based placeholders (like subtitles, paragraphs, captions, list items, process steps, timeline descriptions).
    *   *Requires inputs like:* `layout`, `title`, `content`, `slide_layouts`.
    *   *Outputs:* Plain text.
*   *{ Placeholder for future agents like `image_agent`, `table_agent`, `chart_agent`, `media_agent` - Assume they exist conceptually and follow a similar pattern: requiring context (like title, content) and outputting structured data or references (image paths, table data JSON, chart data JSON, video links). }*

**Your Step-by-Step Process:**

1.  **Analyze Target Layout Schema & Identify Placeholders:**
    *   Look up the definition for `{layout_name}` within the provided `{layouts}`.
    *   Examine its schema carefully to identify **all** placeholders that need content (e.g., `subtitle`, `content`, `colLeft`, `image`, `table`, `chart`, `caption`, `step1Text`, `milestone1Lower`, `media`, `contactInfo`, etc.).
    *   For each placeholder, determine its **required content type** (e.g., 'text', 'image', 'table', 'chart', 'media').

2.  **Iterate Through Placeholders and Invoke Agents:**
    *   Process each placeholder identified in Step 1 one by one.
    *   For a given placeholder:
        *   Determine its required content type ('text', 'image', 'table', etc.).
        *   Identify the **correct specialized agent** from your available pool that handles this content type (e.g., use `text_agent` for 'text' placeholders).
        *   **If** the appropriate agent for the placeholder's type is available in your current list:
            *   Prepare the necessary inputs for that specific agent. Common inputs will likely include `{layout_name}`, `{title}`, and `{content}`, but check the agent's specific requirements if defined.
            *   Invoke the selected agent with the prepared inputs.
            *   Store the content returned by the agent (this could be plain text, JSON data, a URL, etc.).
        *   **If** the agent needed for a placeholder's type is *not* currently available (e.g., you need an `image_agent` but only have `text_agent`):
            *   Note this placeholder and its type. You will handle it in the assembly step.

3.  **Assemble Final Slide Data:**
    *   Construct the final JSON object for the slide, strictly following the schema defined for `{layout_name}` in `{layouts}`.
    *   Populate the `layout` field with `{layout_name}`.
    *   Populate the `title` field with `{title}`.
    *   For each placeholder identified in Step 1:
        *   If you successfully invoked an agent and received content for it in Step 2, insert that generated content into the corresponding field in the JSON object.
        *   If the required agent was unavailable (as noted in Step 2), represent this in the JSON object appropriately (e.g., leave the field as `null`, or use a placeholder object like `{"type": "image", "status": "agent_unavailable"}`).

**Output:**
Your final output should be the complete JSON data structure for the single slide defined by `{layout_name}` and `{title}`, populated with content generated by the available specialized agents, and indicating where content generation was not possible due to missing agents.

Focus on accurately identifying placeholder types, selecting and invoking the *correct* available agent for each, and assembling the final, structured JSON output based on the results.
"""


Layout_Desc = """
You are an AI assistant that generates slide data in JSON format based on input content, selecting the most appropriate slide layout from a predefined list. Analyze the user's content and choose the best layout(s) to represent it effectively, adhering strictly to the structure and constraints of each layout type as defined below.

Here are the available slide layouts:

**Layout 1: titleSlide**
*   **Description:** The standard opening slide for a presentation. Features a prominent title and a smaller subtitle or tagline. Ideal for introducing the overall topic.
*   **Tips:** Keep the title concise and impactful (aim for 5-10 words). Use the subtitle for a brief elaboration or presenter details. If the main topic title is very long, summarize its core essence for this slide.
*   **Schema:**
    ```json
    {
      "layout": "titleSlide",
      "title": "Enter Your Presentation Title Here",
      "subtitle": "Enter your presentation subtitle or tagline here"
    }
    ```

**Layout 2: contentFull**
*   **Description:** A versatile layout with a title, subtitle, and a main content area spanning the full width of the slide. Suitable for paragraphs of text, bullet points, or a combination.
*   **Tips:** Best used for substantial text content that doesn't need to be broken into columns. Use the subtitle to provide context for the main content. If the text becomes too dense, consider splitting it across multiple `contentFull` slides or using a column layout (`contentTwoCol`, `contentThreeCol`) if the content can be logically divided. Aim for 3-5 key bullet points if using them, following typical presentation best practices.
*   **Schema:**
    ```json
    {
      "layout": "contentFull",
      "title": "Full Width Content Layout",
      "subtitle": "Use this subtitle to provide context for the content below",
      "content": "Enter your main content here...\n\n• Enter your first key point here\n• Enter your second key point here\n• Enter your third key point here"
    }
    ```

**Layout 3: contentTwoCol**
*   **Description:** Divides the content area into two equally sized vertical columns below a main title and subtitle. Each column can have its own heading and content (text, bullets). Good for comparing/contrasting or organizing related points side-by-side.
*   **Tips:** Ensure content is balanced between the two columns for visual appeal. Use clear, concise titles for each column (e.g., "LEFT COLUMN TITLE" / "RIGHT COLUMN TITLE"). If content heavily favors one side, reconsider using `contentFull` or `contentWithMedia`. Strictly adhere to the two-column structure.
*   **Schema:**
    ```json
    {
      "layout": "contentTwoCol",
      "title": "Two Column Layout",
      "subtitle": "Use this subtitle to provide context for both columns",
      "colLeft": "LEFT COLUMN TITLE\n\nEnter content...",
      "colRight": "RIGHT COLUMN TITLE\n\nEnter content..."
    }
    ```

**Layout 4: contentThreeCol**
*   **Description:** Divides the content area into three equally sized vertical columns below a main title and subtitle. Ideal for presenting three related concepts, features, or steps concisely.
*   **Tips:** Keep the content within each column brief due to limited width. Use clear column titles. This layout works best when you have exactly three distinct points to cover. If you have fewer or more, consider `contentTwoCol`, `contentFourCol`, or `contentFull`. Strictly adhere to the three-column structure.
*   **Schema:**
    ```json
    {
      "layout": "contentThreeCol",
      "title": "Three Column Layout",
      "subtitle": "Use this subtitle to introduce the three-column content",
      "colLeft": "COLUMN 1 TITLE\n\nEnter content...",
      "colMiddle": "COLUMN 2 TITLE\n\nEnter content...",
      "colRight": "COLUMN 3 TITLE\n\nEnter content..."
    }
    ```

**Layout 5: contentFourCol**
*   **Description:** Divides the content area into four equally sized vertical columns below a main title and subtitle. Suitable for presenting four brief, related items or categories.
*   **Tips:** Content in each column must be very concise. Best used for keywords, short phrases, or icons with minimal text. Ensure you have exactly four items to present; otherwise, choose a layout with fewer columns. Strictly adhere to the four-column structure.
*   **Schema:**
    ```json
    {
      "layout": "contentFourCol",
      "title": "Four Column Layout",
      "subtitle": "Use this subtitle to introduce the four-column content",
      "col1": "COLUMN 1 TITLE\n\nEnter content",
      "col2": "COLUMN 2 TITLE\n\nEnter content",
      "col3": "COLUMN 3 TITLE\n\nEnter content",
      "col4": "COLUMN 4 TITLE\n\nEnter content"
    }
    ```

**Layout 6: contentWithMediaRight**
*   **Description:** Places explanatory text on the left side and a media element (image or video placeholder) on the right, below a title and subtitle. Good for visually illustrating a concept described in the text.
*   **Tips:** Ensure the media directly relates to and enhances the text content. Keep the text focused and reasonably concise (aim for 1-2 paragraphs). The media placeholder is roughly square/4:3; choose images that fit well.
*   **Schema:**
    ```json
    {
      "layout": "contentWithMediaRight",
      "title": "Text Left, Media Right",
      "subtitle": "Use this subtitle to introduce the content and image",
      "content": "Enter your explanatory text here...\n\nAdd a second paragraph if needed...",
      "media": {
        "path": "path/to/your/image.jpg", // or video
        "type": "image" // or "video"
      }
    }
    ```

**Layout 7: contentWithMediaLeft**
*   **Description:** Places a media element (image or video placeholder) on the left side and explanatory text on the right, below a title and subtitle. Useful when you want the visual element to be seen first or take slight precedence.
*   **Tips:** Similar to `contentWithMediaRight`, ensure media relevance. Keep text concise. The layout provides a balanced look. Choose media that fits the roughly square/4:3 placeholder well.
*   **Schema:**
    ```json
    {
      "layout": "contentWithMediaLeft",
      "title": "Media Left, Text Right",
      "subtitle": "Use this subtitle to introduce the image and content",
      "content": "Enter your explanatory text here...\n\nAdd a second paragraph if needed...",
      "media": {
        "path": "path/to/your/image.jpg", // or video
        "type": "image" // or "video"
      }
    }
    ```

**Layout 8: imageWithCaption**
*   **Description:** Features a large, prominent image area spanning most of the slide width, with a title above and a caption area below. Ideal for showcasing a single, impactful image.
*   **Tips:** Use high-quality images that work well in a wide aspect ratio (approx. 16:9 or wider). The caption should be descriptive, explaining what the audience is seeing and its significance, but keep it concise (1-2 sentences recommended).
*   **Schema:**
    ```json
    {
      "layout": "imageWithCaption",
      "title": "Image with Caption",
      "image": {
        "path": "path/to/your/image.jpg",
        "type": "image"
      },
      "caption": "Enter a descriptive caption for your image here..."
    }
    ```

**Layout 9: videoWithCaption**
*   **Description:** Designed to prominently display a video (represented by a placeholder) with a title above. The schema also includes a caption field, though its visual prominence may vary.
*   **Tips:** Ideal for embedding or linking to a key video. Ensure the video source/link is correct. Use the title to introduce the video's topic. Provide a concise caption (if the schema's `caption` field is used visually) to add context or source information. The placeholder suggests a wide aspect ratio (like 16:9).
*   **Schema:**
    ```json
    {
      "layout": "videoWithCaption",
      "title": "Video Presentation",
      "media": {
        "path": "path/to/your/video.mp4", // or youtube embed link, check implementation
        "type": "video" // or "online" if using links
      },
      "caption": "Enter a descriptive caption for your featured video" // Optional, depending on visual need
    }
    ```

**Layout 10: imageGrid**
*   **Description:** Displays multiple images in a grid format below a title. A common configuration is a 2-row, 3-column grid (6 images total).
*   **Tips:** Use this when you need to show a collection of related images (e.g., product variations, team members, visual examples). Ensure all images have a similar aspect ratio (roughly square or 4:3) for consistency. Strictly adhere to the intended grid structure (e.g., 2x3); if you have a different number of images, this layout may require modification or leaving placeholders blank.
*   **Schema:**
    ```json
    {
      "layout": "imageGrid",
      "title": "Image Grid Layout",
      "cell_1_1": { "path": "...", "type": "image" },
      "cell_1_2": { "path": "...", "type": "image" },
      "cell_1_3": { "path": "...", "type": "image" },
      "cell_2_1": { "path": "...", "type": "image" },
      "cell_2_2": { "path": "...", "type": "image" },
      "cell_2_3": { "path": "...", "type": "image" }
    }
    ```

**Layout 11: table**
*   **Description:** Presents tabular data clearly with a title and subtitle. Typically includes a header row and several data rows.
*   **Tips:** Ideal for structured numerical data, comparisons, or feature lists. Be mindful of the number of rows and columns that fit comfortably on a slide (e.g., aim for around 4-6 columns and 4-5 data rows as a guideline). If your data has significantly more rows/columns, it may become cramped. Consider simplifying the data, splitting it across multiple tables/slides, or choosing a different visualization (like a chart) if appropriate. Keep cell content concise. The `options` field allows for styling customization.
*   **Schema:**
    ```json
    {
      "layout": "table",
      "title": "Table Layout",
      "subtitle": "Provide context for the table data",
      "table": {
        "rows": [
          ["Header 1", "Header 2", "Header 3", "Header 4", "Header 5", "Header 6"],
          ["Row1 Data1", "Row1 Data2", "Row1 Data3", "Row1 Data4", "Row1 Data5", "Row1 Data6"],
          // ... more rows (aim for ~4 data rows)
        ],
        "options": { // Optional styling
          // "columnWidths": [...],
          // "border": {...},
          // "headerRow": true, ... etc.
        }
      }
    }
    ```

**Layout 12: chartSingle**
*   **Description:** Displays a single chart (e.g., line, bar, pie) with a title, subtitle, and an area for explanatory text or key insights.
*   **Tips:** Choose the chart type (`line`, `bar`, `pie`, `area`, `scatter`, `doughnut`) that best represents the data trend or comparison. Use the subtitle to specify what the chart shows (e.g., units, time period). The "Key Insights" area is crucial – use it to explicitly state the main takeaways from the chart data (2-4 bullet points recommended). Ensure data labels and values are clear.
*   **Schema:**
    ```json
    {
      "layout": "chartSingle",
      "title": "Single Chart Layout",
      "subtitle": "Describe the chart's focus (e.g., Sales performance by region...)",
      "chart": {
        "type": "line", // e.g., "bar", "pie", "doughnut", "area"
        "data": [
          {
            "name": "Series Name",
            "labels": ["Label1", "Label2", ...],
            "values": [Value1, Value2, ...]
          }
          // Potentially more series for line/bar charts
        ]
        // Add chart options if needed (colors, axis titles etc.)
      },
      "explanationTitle": "Key Insights",
      "explanationContent": "• Insight 1...\n• Insight 2..."
    }
    ```

**Layout 13: chartDual**
*   **Description:** Presents two charts side-by-side under a main title. Each chart area has its own title and a brief explanation below it.
*   **Tips:** Ideal for comparing two related datasets or showing data from two different perspectives/time periods. Choose appropriate chart types for each side. Keep the individual chart titles (`titleLeft`, `titleRight`) concise and the explanations (`explanationLeft`, `explanationRight`) brief (1-2 sentences each). Ensure the charts are visually balanced.
*   **Schema:**
    ```json
    {
      "layout": "chartDual",
      "title": "Dual Chart Layout",
      "titleLeft": "Left Chart Title",
      "titleRight": "Right Chart Title",
      "chartLeft": {
        "type": "doughnut", // or other type
        "data": [{ "name": "...", "labels": [...], "values": [...] }]
        // Options
      },
      "chartRight": {
        "type": "pie", // or other type
        "data": [{ "name": "...", "labels": [...], "values": [...] }]
        // Options
      },
      "explanationLeft": "Explanation for left chart...",
      "explanationRight": "Explanation for right chart..."
    }
    ```

**Layout 14: dashboard**
*   **Description:** Displays multiple (typically four) charts together in a grid format under a main title, resembling a dashboard.
*   **Tips:** Use this to provide a high-level overview of several key metrics or data points simultaneously. Keep each chart relatively simple due to limited space. Ensure chart types are appropriate for the data they represent. Titles for individual charts are usually embedded within the chart object (`name` field in data or specific chart options) rather than separate text fields in this layout schema. Strictly adhere to the intended multi-chart structure (e.g., four charts). If you have fewer key metrics, another layout might be better.
*   **Schema:**
    ```json
    {
      "layout": "dashboard",
      "title": "Dashboard Layout",
      "chart1": { "type": "line", "data": [...] /* ... */ },
      "chart2": { "type": "bar", "data": [...] /* ... */ },
      "chart3": { "type": "area", "data": [...] /* ... */ },
      "chart4": { "type": "pie", "data": [...] /* ... */ }
    }
    ```

**Layout 15: processHorizontal**
*   **Description:** Illustrates a linear process with distinct stages arranged horizontally, often represented by boxes connected by arrows, with descriptive text below each stage.
*   **Tips:** Ideal for showing sequential steps, workflows, or phases (typically 3-5 stages fit well horizontally). Clearly label each stage in the `stepXBox` fields. Keep the descriptive text (`stepXText`) concise and focused on the actions/outcomes of that stage. This layout works best for a fixed number of stages (e.g., four); if your process differs significantly, consider `processVertical` or another visualization. Strictly adhere to the intended number of horizontal stages.
*   **Schema:**
    ```json
    {
      "layout": "processHorizontal",
      "title": "Horizontal Process Layout",
      "step1Box": "Stage 1 Title",
      "step2Box": "Stage 2 Title",
      "step3Box": "Stage 3 Title",
      "step4Box": "Stage 4 Title", // Adjust number of steps as needed/supported
      "step1Text": "Description for stage 1...",
      "step2Text": "Description for stage 2...",
      "step3Text": "Description for stage 3...",
      "step4Text": "Description for stage 4..."
      // Arrow properties are likely predefined by the template/theme
    }
    ```

**Layout 16: processVertical**
*   **Description:** Illustrates a linear process with stages arranged vertically, often as boxes connected by downward arrows, with descriptive text placed beside each stage box.
*   **Tips:** Suitable for sequential processes (typically 3-5 stages fit well vertically), especially when descriptions for each stage are slightly longer. Clearly label each stage (`stepXBox`). Use the `stepXText` for descriptions, including relevant details like timelines if applicable. This layout is best suited for a specific number of stages (e.g., three); adapt content accordingly or choose another layout if the number differs significantly. Strictly adhere to the intended number of vertical stages.
*   **Schema:**
    ```json
    {
      "layout": "processVertical",
      "title": "Vertical Process Layout",
      "step1Box": "Stage 1 Title",
      "step2Box": "Stage 2 Title",
      "step3Box": "Stage 3 Title", // Adjust number of steps as needed/supported
      "step1Text": "Description for stage 1 (e.g., timeline)...",
      "step2Text": "Description for stage 2 (e.g., timeline)...",
      "step3Text": "Description for stage 3 (e.g., timeline)..."
      // Arrow properties are likely predefined
    }
    ```

**Layout 17: timelineHorizontal**
*   **Description:** Displays key milestones or events along a horizontal timeline bar, typically with markers for each milestone. Each milestone often has a date/title above the bar and a description below.
*   **Tips:** Excellent for project roadmaps, historical timelines, or sequential event summaries (typically 3-5 milestones fit well). Use the `milestoneXUpper` fields for dates and brief event titles. Use `milestoneXLower` for concise descriptions of what happened at that milestone. This layout is structured for a specific number of milestones (e.g., four); ensure your content fits this structure or consider alternatives. Strictly adhere to the intended number of horizontal milestones.
*   **Schema:**
    ```json
    {
      "layout": "timelineHorizontal",
      "title": "Horizontal Timeline Layout",
      // Timeline bar and milestone marker colors/styles likely predefined
      "milestone1Upper": "Date / Event 1 Title",
      "milestone2Upper": "Date / Event 2 Title",
      "milestone3Upper": "Date / Event 3 Title",
      "milestone4Upper": "Date / Event 4 Title", // Adjust number as needed/supported
      "milestone1Lower": "Description for milestone 1...",
      "milestone2Lower": "Description for milestone 2...",
      "milestone3Lower": "Description for milestone 3...",
      "milestone4Lower": "Description for milestone 4..."
    }
    ```

**Layout 18: timelineVertical**
*   **Description:** Displays key milestones or events along a vertical timeline bar, usually with markers. Each milestone typically has a date indicator to one side and a description on the other.
*   **Tips:** Useful for chronological sequences (typically 3-5 milestones fit well vertically), especially when descriptions are slightly more detailed. Use `milestoneXDate` for the time indicator (e.g., Q1 2024, Year). Use `milestoneXText` for the description of events/achievements at that point. This layout is structured for a specific number of milestones (e.g., four). If your timeline differs significantly, consider if this layout is still the best fit. Strictly adhere to the intended number of vertical milestones.
*   **Schema:**
    ```json
    {
      "layout": "timelineVertical",
      "title": "Vertical Timeline Layout",
      // Timeline bar and milestone marker colors/styles likely predefined
      "milestone1Date": "Date/Period 1",
      "milestone2Date": "Date/Period 2",
      "milestone3Date": "Date/Period 3",
      "milestone4Date": "Date/Period 4", // Adjust number as needed/supported
      "milestone1Text": "Description for milestone 1...",
      "milestone2Text": "Description for milestone 2...",
      "milestone3Text": "Description for milestone 3...",
      "milestone4Text": "Description for milestone 4..."
    }
    ```

**Layout 19: contactInfo**
*   **Description:** A concluding slide, typically used for 'Thank You' messages, contact information, or a call to action. Features a main message and a block for contact details.
*   **Tips:** Keep the `thankYouText` clear and simple. Format the `contactInfo` for readability, including name, role/company, email, and website/social links as needed, using line breaks (`\n`) for separation.
*   **Schema:**
    ```json
    {
      "layout": "contactInfo",
      "thankYouText": "Thank You. End of Presentation",
      "contactInfo": "John Doe\nRole XYZ\nEmail: john.doe@company.com\nwww.company.com"
    }
    ```

**General Instructions:**
1.  Receive the raw content from the user.
2.  Analyze the content's structure, key points, data types (text, lists, images, tables, charts, processes, timelines), and volume.
3.  Select the most appropriate layout(s) from the list above that best represent the content visually and structurally, paying close attention to the specific constraints mentioned in the tips (e.g., number of columns, rows, stages, milestones).
4.  Populate the corresponding JSON schema for the chosen layout(s) with the user's content, adapting phrasing or summarizing where necessary to fit the layout constraints.
5.  If content is too large for a single slide layout, recommend splitting it across multiple slides of the same or appropriate different types.
6.  If numerical data is present but unstructured, consider if `table` or a `chart` layout is suitable. Only recommend chart layouts if the data lends itself to meaningful visualization (trends, comparisons, proportions).
7.  Output the final slide data as a JSON array.

"""
Layout_Schema = """
const sampleData = {
  title: "PPTxGenJS Presentation",
  subject: "Sample Presentation",
  author: "Edunova",
  theme: "default", 
  slides: [
    // Title and Basic Layouts Section
    {
      layout: "titleSlide", 
      title: "Enter Your Presentation Title Here",
      subtitle: "Enter your presentation subtitle or tagline here",
    },

    {
      layout: "contentFull",
      title: "Full Width Content Layout",
      subtitle: "Use this subtitle to provide context for the content below",
      content: "Enter your main content here. This layout uses the entire width of the slide for content. It's ideal for large blocks of text, wide images, or when you need maximum space for your content.\n\n• Enter your first key point here\n• Enter your second key point here\n• Enter your third key point here"
    },
    
    {
      layout: "contentTwoCol",
      title: "Two Column Layout",
      subtitle: "Use this subtitle to provide context for both columns",
      colLeft: "LEFT COLUMN TITLE\n\nEnter content for the left column here. You can place text, bullet points, or other content in this section.",
      colRight: "RIGHT COLUMN TITLE\n\nEnter content for the right column here. The two columns are equally sized and provide good visual balance."
    },
    
    {
      layout: "contentThreeCol",
      title: "Three Column Layout", 
      subtitle: "Use this subtitle to introduce the three-column content",
      colLeft: "COLUMN 1 TITLE\n\nEnter first column content here.",
      colMiddle: "COLUMN 2 TITLE\n\nEnter second column content here.",
      colRight: "COLUMN 3 TITLE\n\nEnter third column content here."
    },
    
    {
      layout: "contentFourCol",
      title: "Four Column Layout",
      subtitle: "Use this subtitle to introduce the four-column content",
      col1: "COLUMN 1 TITLE\n\nEnter content here",
      col2: "COLUMN 2 TITLE\n\nEnter content here", 
      col3: "COLUMN 3 TITLE\n\nEnter content here",
      col4: "COLUMN 4 TITLE\n\nEnter content here"
    },
    
    {
      layout: "contentWithMediaRight",
      title: "Text Left, Media Right",
      subtitle: "Use this subtitle to introduce the content and image",
      content: "Enter your explanatory text here. This layout places text on the left side with supporting media on the right.\n\nAdd a second paragraph here if needed to explain your concept fully.",
      media: {
        path: "./src/assets/image.jpg",
        type: "image"
      }
    },
    
    {
      layout: "contentWithMediaLeft",
      title: "Media Left, Text Right",
      subtitle: "Use this subtitle to introduce the image and content",
      content: "Enter your explanatory text here. This layout places visual media on the left with explanatory text on the right.\n\nAdd a second paragraph here if needed to explain the visual element.",
      media: {
        path: "./src/assets/image.jpg",
        type: "image"
      }
    },
    
    {
      layout: "imageWithCaption",
      title: "Image with Caption",
      image: {
        path: "./src/assets/image.jpg",
        type: "image"
      },
      caption: "Enter a descriptive caption for your image here. Explain what the audience is seeing and why it matters."
    },
    
    {
      layout: "videoWithCaption",
      title: "Video Presentation",
      media: {
        path: "./src/assets/image.jpg",
        type: "image"
      },
      caption: "Enter a descriptive caption for your featured video"
    },
    
    {
      layout: "imageGrid",
      title: "Image Grid Layout",
      cell_1_1: {
        path: "./src/assets/image.jpg",
        type: "image"
      },
      cell_1_2: {
        path: "./src/assets/image.jpg",
        type: "image"
      },
      cell_1_3: {
        path: "./src/assets/image.jpg",
        type: "image"
      },
      cell_2_1: {
        path: "./src/assets/image.jpg",
        type: "image"
      },
      cell_2_2: {
        path: "./src/assets/image.jpg",
        type: "image"
      },
      cell_2_3: {
        path: "./src/assets/image.jpg",
        type: "image"
      }
    },
    
    {
      layout: "table",
      title: "Table Layout",
      subtitle: "Quarterly breakdown of sales performance in thousands ($)",
      table: {
        rows: [
          ["Product Category", "Q1 Sales", "Q2 Sales", "Q3 Sales", "Q4 Sales", "Total"],
          ["Electronics", "$245", "$251", "$264", "$290", "$1,050"],
          ["Furniture", "$110", "$125", "$150", "$180", "$565"],
          ["Office Supplies", "$196", "$201", "$210", "$203", "$810"],
          ["Total", "$551", "$577", "$624", "$673", "$2,425"]
        ],
        options: {
          columnWidths: [2, 1.5, 1.5, 1.5, 1.5, 1],
          autoPageRepeat: false,
          autoPageSlides: false,
          fontFace: "Arial",
          fontSize: 12,
          color: "363636",
          border: { type: "solid", pt: 1, color: "808080" },
          headerRow: true,
          headerRowOptions: {
            fontFace: "Arial",
            fontSize: 14,
            bold: true,
            color: "FFFFFF",
            fill: { color: "404040" }
          },
          zebra: true,
          zebraColors: ['F5F5F5', 'FFFFFF']
        }
      }
    },
    
    {
      layout: "chartSingle",
      title: "Single Chart Layout",
      subtitle: "Sales performance by region in millions ($)",
      chart: {
        type: "line",
        data: [
          {
            name: "2024 Regional Sales",
            labels: ["North", "East", "South", "West", "Central"],
            values: [28, 39, 23, 45, 35]
          }
        ]
      },
      explanationTitle: "Key Insights",
      explanationContent: "• West region shows strongest performance at $45M\n• East region is second at $39M\n• South region is underperforming at $23M\n• Overall regional average is $34M"
    },
    
    {
      layout: "chartDual",
      title: "Dual Chart Layout",
      titleLeft: "2023 Sales Distribution",
      titleRight: "2024 Sales Distribution",
      chartLeft: {
        type: "doughnut",
        data: [
          {
            name: "2023 Product Categories",
            labels: ["Electronics", "Furniture", "Office Supplies", "Services", "Software"],
            values: [45, 20, 15, 10, 10]
          }
        ]
      },
      chartRight: {
        type: "pie",
        data: [
          {
            name: "2024 Product Categories",
            labels: ["Electronics", "Furniture", "Office Supplies", "Services", "Software"],
            values: [40, 15, 15, 15, 15]
          }
        ]
      },
      explanationLeft: "2023: Electronics dominated at 45%, with Furniture following at 20%. Office Supplies, Services and Software were minor segments.",
      explanationRight: "2024: Electronics reduced to 40%, while Services and Software increased to 15% each, showing diversification."
    },
    
    {
      layout: "dashboard",
      title: "Dashboard Layout",
      chart1: {
        type: "line",
        data: [
          {
            name: "Quarterly Revenue (millions $)",
            labels: ["Q1", "Q2", "Q3", "Q4"],
            values: [45, 52, 59, 63]
          }
        ]
      },
      chart2: {
        type: "bar",
        data: [
          {
            name: "Monthly Active Users (thousands)",
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            values: [1452, 1836, 2107, 2350, 2620, 2840]
          }
        ]
      },
      chart3: {
        type: "area",
        data: [
          {
            name: "Market Share (%)",
            labels: ["Q1-23", "Q2-23", "Q3-23", "Q4-23", "Q1-24", "Q2-24"],
            values: [25, 30, 35, 40, 45, 47]
          }
        ]
      },
      chart4: {
        type: "pie",
        data: [
          {
            name: "Device Usage Distribution",
            labels: ["Desktop", "Mobile", "Tablet"],
            values: [55, 35, 10]
          }
        ]
      }
    },
    
    {
      layout: "processHorizontal",
      title: "Horizontal Process Layout",
      step1Box: "Research",
      step2Box: "Design",
      step3Box: "Development",
      step4Box: "Launch",
      step1Text: "Market analysis, customer interviews, and requirements gathering",
      step2Text: "Create prototypes, test with users, and refine specifications",
      step3Text: "Build the product, perform quality assurance, and prepare marketing",
      step4Text: "Release product, collect feedback, and plan future improvements",
      arrow1: { type: "right-arrow", color: "#404040" },
      arrow2: { type: "right-arrow", color: "#404040" },
      arrow3: { type: "right-arrow", color: "#404040" }
    },
    
    {
      layout: "processVertical",
      title: "Vertical Process Layout",
      step1Box: "Planning",
      step2Box: "Execution",
      step3Box: "Evaluation",
      step1Text: "Define project scope, create timeline, allocate resources, and assign responsibilities to team members (Jan-Feb 2024)",
      step2Text: "Implement solution, monitor progress, make adjustments, and maintain regular stakeholder communication (Mar-Aug 2024)",
      step3Text: "Assess outcomes, document lessons learned, and plan for ongoing maintenance and future enhancements (Sep-Dec 2024)",
      arrow1: { type: "down-arrow", color: "#404040" },
      arrow2: { type: "down-arrow", color: "#404040" }
    },
    
    {
      layout: "timelineHorizontal",
      title: "Horizontal Timeline Layout",
      timelineBar: { color: "#404040" },
      milestone1: { color: "#5DA5DA" },
      milestone2: { color: "#FAA43A" },
      milestone3: { color: "#60BD68" },
      milestone4: { color: "#F17CB0" },
      milestone1Upper: "January 2024\nProject Kickoff",
      milestone2Upper: "March 2024\nMVP Release",
      milestone3Upper: "July 2024\nBeta Launch",
      milestone4Upper: "October 2024\nFull Release",
      milestone1Lower: "Team formation, requirements gathering, and initial planning completed",
      milestone2Lower: "Core functionality developed and tested with internal stakeholders",
      milestone3Lower: "Limited release to beta testers with formal feedback collection",
      milestone4Lower: "Public launch with comprehensive marketing campaign"
    },
    
    {
      layout: "timelineVertical",
      title: "Vertical Timeline Layout",
      timelineBar: { color: "#404040" },
      milestone1: { color: "#5DA5DA" },
      milestone2: { color: "#FAA43A" },
      milestone3: { color: "#60BD68" },
      milestone4: { color: "#F17CB0" },
      milestone1Date: "Q1 2024",
      milestone2Date: "Q2 2024",
      milestone3Date: "Q3 2024",
      milestone4Date: "Q4 2024",
      milestone1Text: "New office opening, hiring of 15 additional team members, launch of R&D department",  
      milestone2Text: "Series B funding secured, expansion into European market, partnership with key industry players",
      milestone3Text: "Release of next-generation product line, acquisition of competitor startup, 50% growth in customer base",
      milestone4Text: "IPO preparation, opening of international headquarters, annual revenue target surpassed"
    },

    
    {
      layout: "contactInfo",
      thankYouText: "Thank You. End of Presentation",
      contactInfo: "John Doe\nRole XYZ\nEmail: john.doe@company.com\nwww.company.com"
    }
  ]
};

module.exports = sampleData;
"""

Content = """
Climate change is one of the most pressing issues of our time, and its impact on biodiversity is profound and far-reaching. As global temperatures rise, ecosystems are being altered, species are facing extinction, and the delicate balance of nature is being disrupted.

The effects of climate change on biodiversity are evident in various ways. For instance, many species are experiencing shifts in their habitats as they attempt to adapt to changing temperatures and weather patterns. This can lead to mismatches in the timing of life cycle events, such as flowering and pollination, which can have cascading effects on entire ecosystems.
"""
