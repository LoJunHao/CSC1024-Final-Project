Social Media Content Planner & Performance Reporter
An easy-to-digest technical and operational guide for the Social Media Content Planner project. This project is a command-line interface (CLI) tool designed to manage social media posts, track post lifecycle status, record engagement metrics, and compile performance reports.

🛠️ Project Structure & Architecture
The application is structured as a single-executable Python CLI utility that leverages plain-text flat files as its persistent database layer.
Directory Layout

planner.py — Core application entry point, containing data handlers, validation logic, CLI menus, and business logic.
test_planner.py — Unit test suite verifying platform/post loading, data schema integrity, and report compilation.
platforms.txt — Flat-file database storing details of target platforms.
posts.txt — Flat-file database storing post ideas, captions, schedules, and lifecycle status.
engagement.txt — Flat-file database storing likes, comments, shares, and views for published posts.


📊 Database & Data Schemas
The database uses pipe-delimited (|) values to separate fields. Data is read, updated, and saved sequentially.
1. Platforms Schema (platforms.txt)
Stores the available channels and their current follower counts.

Format: Platform ID|Platform Name|Follower Count
Example:
P1|Instagram|12500P2|TikTok|45000P3|X|8200


2. Posts Schema (posts.txt)
Tracks post attributes, scheduling dates, and their publishing status.

Format: Post ID|Platform Name|Content Caption|Scheduled Date|Status
Example:
POST001|Instagram|Check out our new project launch!|2026-08-01|ScheduledPOST002|TikTok|A day in the life of a computer science student|2026-07-10|Posted


3. Engagement Schema (engagement.txt)
Stores raw metric logs for posted content to compute performance summaries.

Format: Post ID|Likes|Comments|Shares|Views
Example:
POST002|1200|85|45|15000POST003|150|12|8|850



🔄 Post Status Lifecycle
Posts navigate through three main states. Status logic prevents recording metrics until a post reaches the terminal Posted state.
#mermaid-diagram-0-y5d492vp8hb{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-diagram-0-y5d492vp8hb .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-diagram-0-y5d492vp8hb .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-diagram-0-y5d492vp8hb .error-icon{fill:#552222;}#mermaid-diagram-0-y5d492vp8hb .error-text{fill:#552222;stroke:#552222;}#mermaid-diagram-0-y5d492vp8hb .edge-thickness-normal{stroke-width:1px;}#mermaid-diagram-0-y5d492vp8hb .edge-thickness-thick{stroke-width:3.5px;}#mermaid-diagram-0-y5d492vp8hb .edge-pattern-solid{stroke-dasharray:0;}#mermaid-diagram-0-y5d492vp8hb .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-diagram-0-y5d492vp8hb .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-diagram-0-y5d492vp8hb .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-diagram-0-y5d492vp8hb .marker{fill:#333333;stroke:#333333;}#mermaid-diagram-0-y5d492vp8hb .marker.cross{stroke:#333333;}#mermaid-diagram-0-y5d492vp8hb svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-diagram-0-y5d492vp8hb p{margin:0;}#mermaid-diagram-0-y5d492vp8hb defs #statediagram-barbEnd{fill:#333333;stroke:#333333;}#mermaid-diagram-0-y5d492vp8hb g.stateGroup text{fill:#9370DB;stroke:none;font-size:10px;}#mermaid-diagram-0-y5d492vp8hb g.stateGroup text{fill:#333;stroke:none;font-size:10px;}#mermaid-diagram-0-y5d492vp8hb g.stateGroup .state-title{font-weight:bolder;fill:#131300;}#mermaid-diagram-0-y5d492vp8hb g.stateGroup rect{fill:#ECECFF;stroke:#9370DB;}#mermaid-diagram-0-y5d492vp8hb g.stateGroup line{stroke:#333333;stroke-width:1;}#mermaid-diagram-0-y5d492vp8hb .transition{stroke:#333333;stroke-width:1;fill:none;}#mermaid-diagram-0-y5d492vp8hb .stateGroup .composit{fill:white;border-bottom:1px;}#mermaid-diagram-0-y5d492vp8hb .stateGroup .alt-composit{fill:#e0e0e0;border-bottom:1px;}#mermaid-diagram-0-y5d492vp8hb .state-note{stroke:#aaaa33;fill:#fff5ad;}#mermaid-diagram-0-y5d492vp8hb .state-note text{fill:black;stroke:none;font-size:10px;}#mermaid-diagram-0-y5d492vp8hb .stateLabel .box{stroke:none;stroke-width:0;fill:#ECECFF;opacity:0.5;}#mermaid-diagram-0-y5d492vp8hb .edgeLabel .label rect{fill:#ECECFF;opacity:0.5;}#mermaid-diagram-0-y5d492vp8hb .edgeLabel{background-color:rgba(232,232,232, 0.8);text-align:center;}#mermaid-diagram-0-y5d492vp8hb .edgeLabel p{background-color:rgba(232,232,232, 0.8);}#mermaid-diagram-0-y5d492vp8hb .edgeLabel rect{opacity:0.5;background-color:rgba(232,232,232, 0.8);fill:rgba(232,232,232, 0.8);}#mermaid-diagram-0-y5d492vp8hb .edgeLabel .label text{fill:#333;}#mermaid-diagram-0-y5d492vp8hb .label div .edgeLabel{color:#333;}#mermaid-diagram-0-y5d492vp8hb .stateLabel text{fill:#131300;font-size:10px;font-weight:bold;}#mermaid-diagram-0-y5d492vp8hb .node circle.state-start{fill:#333333;stroke:#333333;}#mermaid-diagram-0-y5d492vp8hb .node .fork-join{fill:#333333;stroke:#333333;}#mermaid-diagram-0-y5d492vp8hb .node circle.state-end{fill:#9370DB;stroke:white;stroke-width:1.5;}#mermaid-diagram-0-y5d492vp8hb .end-state-inner{fill:white;stroke-width:1.5;}#mermaid-diagram-0-y5d492vp8hb .node rect{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-diagram-0-y5d492vp8hb .node polygon{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-diagram-0-y5d492vp8hb #statediagram-barbEnd{fill:#333333;}#mermaid-diagram-0-y5d492vp8hb .statediagram-cluster rect{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-diagram-0-y5d492vp8hb .cluster-label,#mermaid-diagram-0-y5d492vp8hb .nodeLabel{color:#131300;}#mermaid-diagram-0-y5d492vp8hb .statediagram-cluster rect.outer{rx:5px;ry:5px;}#mermaid-diagram-0-y5d492vp8hb .statediagram-state .divider{stroke:#9370DB;}#mermaid-diagram-0-y5d492vp8hb .statediagram-state .title-state{rx:5px;ry:5px;}#mermaid-diagram-0-y5d492vp8hb .statediagram-cluster.statediagram-cluster .inner{fill:white;}#mermaid-diagram-0-y5d492vp8hb .statediagram-cluster.statediagram-cluster-alt .inner{fill:#f0f0f0;}#mermaid-diagram-0-y5d492vp8hb .statediagram-cluster .inner{rx:0;ry:0;}#mermaid-diagram-0-y5d492vp8hb .statediagram-state rect.basic{rx:5px;ry:5px;}#mermaid-diagram-0-y5d492vp8hb .statediagram-state rect.divider{stroke-dasharray:10,10;fill:#f0f0f0;}#mermaid-diagram-0-y5d492vp8hb .note-edge{stroke-dasharray:5;}#mermaid-diagram-0-y5d492vp8hb .statediagram-note rect{fill:#fff5ad;stroke:#aaaa33;stroke-width:1px;rx:0;ry:0;}#mermaid-diagram-0-y5d492vp8hb .statediagram-note rect{fill:#fff5ad;stroke:#aaaa33;stroke-width:1px;rx:0;ry:0;}#mermaid-diagram-0-y5d492vp8hb .statediagram-note text{fill:black;}#mermaid-diagram-0-y5d492vp8hb .statediagram-note .nodeLabel{color:black;}#mermaid-diagram-0-y5d492vp8hb .statediagram .edgeLabel{color:red;}#mermaid-diagram-0-y5d492vp8hb #dependencyStart,#mermaid-diagram-0-y5d492vp8hb #dependencyEnd{fill:#333333;stroke:#333333;stroke-width:1;}#mermaid-diagram-0-y5d492vp8hb .statediagramTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-diagram-0-y5d492vp8hb :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}Added (Default)Transition 1RevertTransition 2Locked (Metrics Active)DraftScheduledPosted

[!NOTE]
Metrics can only be logged for posts with a Posted status. Attempts to log engagement for Draft or Scheduled statuses are blocked.


🚀 Core Functionalities & Workflows
➕ 1. Add Post Idea

Validates uniqueness of Post ID.
Forces target platform selection from the curated list in platforms.txt.
Sanitizes input to disallow the pipe delimiter (|) in content captions.
Enforces date validation in YYYY-MM-DD format.
Sets status to Draft by default.

🔄 2. Update Post Status

Performs transitions between Draft, Scheduled, and Posted.
Updates the file representation in posts.txt.

📈 3. Record Engagement Metrics

Restricted to posts in Posted state.
Prompts and validates non-negative integers for Likes, Comments, Shares, and Views.
Saves/updates records in engagement.txt.

📅 4. Display Content Calendar

Retrieves all post logs.
Sorts posts chronologically by scheduled date.
Prints formatted tables featuring a truncated caption preview.

🗑️ 5. Delete Post Idea

Triggers cascading deletion: removing the post from posts.txt automatically triggers the cleanup of matching metrics in engagement.txt to keep the database consistent.

📊 6. Performance Report Generation & Export

Computes:

Total Posts Per Platform: Post count breakdown across channels.
Best-Performing Post: Found by maximizing interaction sum (Likes + Comments + Shares + Views).
Top Platform: The channel yielding the highest combined interaction points.


Offers CLI output summary or export as a text report to report.txt.


🧪 Testing & Verification
The suite contains tests validation using Python's built-in unittest library.
To run the verification suite, execute the following command in the project directory:
python -m unittest test_planner.py
Covered Test Cases:

test_load_platforms — Ensures target channels load correctly with correct structures.
test_load_posts — Confirms post data is structured properly.
test_load_engagement — Verifies engagement parsing functions.
test_report — Validates the performance report calculations (ranking algorithms, platform counting, best post identification).
