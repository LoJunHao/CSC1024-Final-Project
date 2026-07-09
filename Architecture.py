"""
Academic Session: May 2026
Course Code: CSC1024 Programming Principles
Project Title: Python-Powered Social Media Content Planner

Description:
    A robust, menu-driven CLI application designed to help content creators plan,
    schedule, and analyze social media posts across various platforms. The program
    uses custom text-file reading and writing mechanisms to ensure persistent storage 
    and incorporates complete input validation routines to protect against unexpected inputs.
"""

import os
from datetime import datetime

# --- DATABASE FILE PATH CONSTANTS ---
POSTS_FILE = "posts.txt"
PLATFORMS_FILE = "platforms.txt"
ENGAGEMENT_FILE = "engagement.txt"


# =====================================================================
# SYSTEM INITIALIZATION & DIRECTORIES
# =====================================================================

def initialize_database():
    """
    Ensures that the primary database files (.txt) exist.
    If files are missing, they are created cleanly with header lines or empty states.
    """
    for file_path in [POSTS_FILE, PLATFORMS_FILE, ENGAGEMENT_FILE]:
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w") as file:
                    # Creating files empty, ready for custom CSV-style records.
                    pass
            except IOError as e:
                print(f"[Critical Error] Failed to initialize file database '{file_path}': {e}")


# =====================================================================
# DATA-PERSISTENCE HELPER FUNCTIONS (FILE I/O)
# =====================================================================

def load_platforms():
    """
    Reads platforms.txt and returns a dictionary of platforms.
    File Format: Platform_ID,Platform_Name,Follower_Count
    
    Returns:
        dict: { "P1": {"name": "Instagram", "followers": 1500}, ... }
    """
    platforms = {}
    if not os.path.exists(PLATFORMS_FILE):
        return platforms

    try:
        with open(PLATFORMS_FILE, "r") as file:
            for line_no, line in enumerate(file, 1):
                stripped = line.strip()
                if not stripped:
                    continue  # Ignore empty lines safely
                
                parts = stripped.split(",")
                if len(parts) == 3:
                    plat_id, name, followers = parts
                    try:
                        platforms[plat_id.strip().upper()] = {
                            "name": name.strip(),
                            "followers": int(followers.strip())
                        }
                    except ValueError:
                        print(f"[Warning] platforms.txt (Line {line_no}): Follower count must be an integer. Skipping row.")
                else:
                    print(f"[Warning] platforms.txt (Line {line_no}): Invalid format. Expected 3 fields, got {len(parts)}.")
    except IOError as e:
        print(f"[Error] Failed to read database '{PLATFORMS_FILE}': {e}")
        
    return platforms


def load_posts():
    """
    Reads posts.txt and returns a list of dictionary objects representing planned posts.
    File Format: Post_ID,Platform_ID,Content_Caption,Scheduled_Date,Status
    
    Returns:
        list: [ {"id": "POST001", "platform_id": "P1", "caption": "...", ...}, ... ]
    """
    posts = []
    if not os.path.exists(POSTS_FILE):
        return posts

    try:
        with open(POSTS_FILE, "r") as file:
            for line_no, line in enumerate(file, 1):
                stripped = line.strip()
                if not stripped:
                    continue
                
                parts = stripped.split(",")
                if len(parts) == 5:
                    p_id, plat_id, caption, date, status = parts
                    posts.append({
                        "id": p_id.strip().upper(),
                        "platform_id": plat_id.strip().upper(),
                        "caption": caption.strip(),
                        "date": date.strip(),
                        "status": status.strip().capitalize()
                    })
                else:
                    print(f"[Warning] posts.txt (Line {line_no}): Invalid format. Expected 5 fields, got {len(parts)}.")
    except IOError as e:
        print(f"[Error] Failed to read database '{POSTS_FILE}': {e}")
        
    return posts


def save_posts(posts):
    """
    Writes the active in-memory list of posts back to posts.txt.
    This overwrites old content to keep status updates, corrections, and deletions updated.
    """
    try:
        with open(POSTS_FILE, "w") as file:
            for post in posts:
                # Compile back to clean CSV style
                line = f"{post['id']},{post['platform_id']},{post['caption']},{post['date']},{post['status']}\n"
                file.write(line)
        return True
    except IOError as e:
        print(f"[Error] Failed to write to database '{POSTS_FILE}': {e}")
        return False


def load_engagement():
    """
    Reads engagement.txt and returns a dictionary mapping post IDs to engagement metrics.
    File Format: Post_ID,Likes,Comments,Shares,Views
    
    Returns:
        dict: { "POST002": {"likes": 1200, "comments": 85, ...}, ... }
    """
    engagement = {}
    if not os.path.exists(ENGAGEMENT_FILE):
        return engagement

    try:
        with open(ENGAGEMENT_FILE, "r") as file:
            for line_no, line in enumerate(file, 1):
                stripped = line.strip()
                if not stripped:
                    continue
                
                parts = stripped.split(",")
                if len(parts) == 5:
                    p_id, likes, comments, shares, views = parts
                    try:
                        engagement[p_id.strip().upper()] = {
                            "likes": int(likes.strip()),
                            "comments": int(comments.strip()),
                            "shares": int(shares.strip()),
                            "views": int(views.strip())
                        }
                    except ValueError:
                        print(f"[Warning] engagement.txt (Line {line_no}): Metrics must be integers. Skipping row.")
                else:
                    print(f"[Warning] engagement.txt (Line {line_no}): Invalid format. Expected 5 fields, got {len(parts)}.")
    except IOError as e:
        print(f"[Error] Failed to read database '{ENGAGEMENT_FILE}': {e}")
        
    return engagement


def save_engagement(engagement):
    """
    Writes the active engagement metrics dictionary back to engagement.txt.
    """
    try:
        with open(ENGAGEMENT_FILE, "w") as file:
            for p_id, metrics in engagement.items():
                line = f"{p_id},{metrics['likes']},{metrics['comments']},{metrics['shares']},{metrics['views']}\n"
                file.write(line)
        return True
    except IOError as e:
        print(f"[Error] Failed to write to database '{ENGAGEMENT_FILE}': {e}")
        return False


# =====================================================================
# USER INPUT VALIDATION ROUTINES
# =====================================================================

def get_validated_date(prompt):
    """
    Prompts the user to enter a date, validating that it matches the YYYY-MM-DD standard format.
    Ensures safe chronological calendar ordering later.
    """
    while True:
        date_input = input(prompt).strip()
        try:
            # Parse the string format to confirm it represents a real calendar date
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print("[Input Error] Invalid date format or real date. Please use YYYY-MM-DD (e.g., 2026-08-02).")


def get_non_empty_string(prompt):
    """
    Prompts the user for text input and ensures that it is not left empty,
    protecting fields from corrupt formatting or blank data values.
    """
    while True:
        value = input(prompt).strip()
        if value:
            # commas inside captions can corrupt our CSV layout, let's swap them to safe spaces or semicolons
            if "," in value:
                value = value.replace(",", ";")
                print("[Formatting Alert] Commas inside entries are auto-converted to ';' to protect file layout.")
            return value
        print("[Input Error] This field cannot be left blank. Please try again.")


def get_positive_int(prompt):
    """
    Prompts the user for an integer, validating that it is a positive whole number
    or zero (ideal for metric inputs like views, comments, likes, and followers).
    """
    while True:
        user_input = input(prompt).strip()
        try:
            val = int(user_input)
            if val >= 0:
                return val
            print("[Input Error] Value must be positive or zero. Please try again.")
        except ValueError:
            print("[Input Error] Non-numeric input identified. Please enter a whole positive number.")


# =====================================================================
# SYSTEM CORE FUNCTIONALITIES
# =====================================================================

def add_new_post():
    """
    Adds a new content planning post to the registry database.
    Performs critical validations: Platform existence, unique post ID checking, date compliance.
    Default Post state: 'Draft'
    """
    print("\n" + "="*50)
    print("             ADD NEW POST IDEA")
    print("="*50)
    
    posts = load_posts()
    platforms = load_platforms()
    
    if not platforms:
        print("\n[Notice] No social media platforms exist. Please register platforms in platforms.txt first.")
        return

    # Display available platform guides
    print("Available Targets:")
    for plat_id, info in platforms.items():
        print(f"  [{plat_id}] {info['name']} (Followers: {info['followers']:,})")
    print("-" * 50)

    # 1. Capture and validate a unique Post ID
    while True:
        post_id = get_non_empty_string("Enter Unique Post ID (e.g., POST004): ").upper()
        # Verify uniqueness
        duplicate = any(post['id'] == post_id for post in posts)
        if duplicate:
            print(f"[ID Collision] Post ID '{post_id}' is already assigned. Choose a unique index.")
        else:
            break

    # 2. Capture and validate Target Platform ID
    while True:
        platform_id = get_non_empty_string("Enter Platform ID to post to: ").upper()
        if platform_id in platforms:
            break
        print(f"[Input Error] Platform ID '{platform_id}' does not exist in registry.")

    # 3. Collect details
    caption = get_non_empty_string("Enter Content Caption / Concept: ")
    scheduled_date = get_validated_date("Enter Scheduled Date (YYYY-MM-DD): ")

    new_post = {
        "id": post_id,
        "platform_id": platform_id,
        "caption": caption,
        "date": scheduled_date,
        "status": "Draft"
    }

    posts.append(new_post)
    if save_posts(posts):
        print(f"\n[Success] Post '{post_id}' saved under status 'Draft'!")
    print("="*50)


def update_post_status():
    """
    Linear status controller flow: Draft -> Scheduled -> Posted.
    Controls the flow of planned items before engagement tracking is unlocked.
    """
    print("\n" + "="*50)
    print("             UPDATE POST STATUS")
    print("="*50)
    
    posts = load_posts()
    if not posts:
        print("No planned entries found in database. Add posts first.")
        print("="*50)
        return

    post_id = get_non_empty_string("Enter Post ID to update: ").upper()
    
    # Locate post in database
    target_post = None
    for post in posts:
        if post['id'] == post_id:
            target_post = post
            break

    if not target_post:
        print(f"[Error] Post ID '{post_id}' not found.")
        print("="*50)
        return

    current_status = target_post['status']
    print(f"\nTarget Post: ID '{post_id}'")
    print(f"Current Status: {current_status}")

    if current_status == "Posted":
        print("[Restriction] Already finalized as 'Posted'. No further status updates can be made.")
        print("="*50)
        return

    print("\nUpdate Path Options:")
    if current_status == "Draft":
        print("  1. Update to: [Scheduled]")
        print("  2. Update to: [Posted]")
        choice = input("Enter decision choice (1 or 2): ").strip()
        if choice == "1":
            target_post['status'] = "Scheduled"
        elif choice == "2":
            target_post['status'] = "Posted"
        else:
            print("[Warning] Invalid option selection. Status left unmodified.")
            return

    elif current_status == "Scheduled":
        print("  1. Update to: [Posted]")
        choice = input("Enter decision choice (1): ").strip()
        if choice == "1":
            target_post['status'] = "Posted"
        else:
            print("[Warning] Invalid option selection. Status left unmodified.")
            return

    if save_posts(posts):
        print(f"\n[Success] Status for '{post_id}' updated to '{target_post['status']}'!")
    print("="*50)


def record_engagement():
    """
    Logs active viewer analytics metrics for posts that are flagged as 'Posted'.
    Stores data structure into engagement.txt.
    """
    print("\n" + "="*50)
    print("           RECORD ENGAGEMENT METRICS")
    print("="*50)
    
    posts = load_posts()
    engagement = load_engagement()

    # Isolate posts with status 'Posted' as eligible for tracking
    posted_ids = [p['id'] for p in posts if p['status'] == 'Posted']

    if not posted_ids:
        print("No post ideas are currently listed as 'Posted'.")
        print("Please set a post's status to 'Posted' before registering metrics.")
        print("="*50)
        return

    print(f"Eligible Posts: {', '.join(posted_ids)}")
    post_id = get_non_empty_string("Enter Post ID to record metrics: ").upper()

    if post_id not in posted_ids:
        print(f"[Error] Post ID '{post_id}' is not marked as 'Posted' or doesn't exist.")
        print("="*50)
        return

    print(f"\nUpdate Analytics for [{post_id}]:")
    likes = get_positive_int("  Enter Likes count: ")
    comments = get_positive_int("  Enter Comments count: ")
    shares = get_positive_int("  Enter Shares count: ")
    views = get_positive_int("  Enter Views count: ")

    # Update or add metrics record
    engagement[post_id] = {
        "likes": likes,
        "comments": comments,
        "shares": shares,
        "views": views
    }

    if save_engagement(engagement):
        print(f"\n[Success] Engagement analytics saved for Post '{post_id}'!")
    print("="*50)


def display_content_calendar():
    """
    Displays all scheduled calendar entries sorted chronologically.
    Includes custom layout truncation to protect terminal formatting structures.
    """
    print("\n" + "="*75)
    print("                         CONTENT SCHEDULING CALENDAR")
    print("="*75)
    
    posts = load_posts()
    platforms = load_platforms()

    if not posts:
        print("No posts found in registry! Populate posts in Option 1.")
        print("="*75)
        return

    # Chronological sort (YYYY-MM-DD comparison as strings)
    sorted_posts = sorted(posts, key=lambda x: x['date'])

    # Display clean table headers
    print(f"{'Date':<12} | {'Post ID':<10} | {'Platform':<12} | {'Status':<11} | {'Caption Preview'}")
    print("-" * 75)

    for p in sorted_posts:
        p_id = p['id']
        p_date = p['date']
        p_status = p['status']
        
        # Get Platform Name
        plat_info = platforms.get(p['platform_id'], {"name": f"Unknown ({p['platform_id']})"})
        plat_name = plat_info['name']

        # Clean display layout for captions
        caption = p['caption']
        if len(caption) > 28:
            caption = caption[:25] + "..."

        print(f"{p_date:<12} | {p_id:<10} | {plat_name:<12} | {p_status:<11} | {caption}")
    
    print("="*75)


def compile_performance_summary():
    """
    Runs metrics processing algorithm across databases.
    Returns calculated outputs in formatted text strings and boolean status.
    """
    posts = load_posts()
    platforms = load_platforms()
    engagement = load_engagement()

    if not posts:
        return "No content in planning databases to compile a performance summary.", False

    summary_lines = []
    summary_lines.append("="*55)
    summary_lines.append("          SOCIAL MEDIA PERFORMANCE SUMMARY")
    summary_lines.append(f"          Compiled on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append("="*55)

    # 1. Total Posts count per Platform ID
    summary_lines.append("\n[1] Total Planned Posts Per Platform:")
    plat_counts = {}
    for p in posts:
        plat_id = p['platform_id']
        # Lookup platform display name
        plat_name = platforms.get(plat_id, {"name": f"Unknown Platform ({plat_id})"})["name"]
        plat_counts[plat_name] = plat_counts.get(plat_name, 0) + 1

    for platform_name, total_posts in plat_counts.items():
        summary_lines.append(f"  - {platform_name:<15} : {total_posts} planned post(s)")

    # 2. Determine Best-Performing post (Formula: Likes + Comments + Shares)
    summary_lines.append("\n[2] Best-Performing Post:")
    top_post_id = None
    top_score = -1

    for p_id, metrics in engagement.items():
        interaction_score = metrics['likes'] + metrics['comments'] + metrics['shares']
        if interaction_score > top_score:
            top_score = interaction_score
            top_post_id = p_id

    if top_post_id and top_score >= 0:
        # Find detail records of the top post
        post_record = next((p for p in posts if p['id'] == top_post_id), None)
        if post_record:
            plat_name = platforms.get(post_record['platform_id'], {"name": "Unknown"})["name"]
            summary_lines.append(f"  - Post ID            : {top_post_id}")
            summary_lines.append(f"  - Platform           : {plat_name}")
            summary_lines.append(f"  - Caption Content    : \"{post_record['caption']}\"")
            summary_lines.append(f"  - Total Engagements  : {top_score:,} points")
            summary_lines.append(f"    (Likes: {engagement[top_post_id]['likes']:,} | Comments: {engagement[top_post_id]['comments']:,} | Shares: {engagement[top_post_id]['shares']:,})")
    else:
        summary_lines.append("  - No finalized posted metrics recorded in database yet.")

    # 3. Determine Platform with most engagement interactions
    summary_lines.append("\n[3] Total Interactions per Platform:")
    plat_interactions = {}
    
    # Initialize interaction counters for all known platforms
    for plat_id, info in platforms.items():
        plat_interactions[info['name']] = 0

    # Map scores
    for p in posts:
        p_id = p['id']
        plat_id = p['platform_id']
        plat_name = platforms.get(plat_id, {"name": f"Unknown ({plat_id})"})["name"]

        score = 0
        if p_id in engagement:
            metrics = engagement[p_id]
            score = metrics['likes'] + metrics['comments'] + metrics['shares']

        plat_interactions[plat_name] = plat_interactions.get(plat_name, 0) + score

    best_platform = None
    max_interaction_score = -1

    for p_name, total_score in plat_interactions.items():
        summary_lines.append(f"  - {p_name:<15} : {total_score:,} cumulative interaction points")
        if total_score > max_interaction_score:
            max_interaction_score = total_score
            best_platform = p_name

    summary_lines.append("\n[Conclusion]")
    if best_platform and max_interaction_score > 0:
        summary_lines.append(f"  -> Platform with peak user interaction: {best_platform}")
    else:
        summary_lines.append("  -> No interaction datasets identified to extract peak platform performance.")

    summary_lines.append("="*55)
    return "\n".join(summary_lines), True


def generate_and_export_report():
    """
    Displays the compiled analytics data and exports the text to a report.txt file.
    """
    report_text, ok = compile_performance_summary()
    print("\n" + report_text)

    if ok:
        try:
            with open("report.txt", "w") as file:
                file.write(report_text)
            print("\n[Export Complete] Summary successfully saved locally as 'report.txt'!")
        except IOError as e:
            print(f"\n[Export Error] Failed to write report file to drive disk: {e}")


# =====================================================================
# SYSTEM APPLICATION EXECUTION CONTEXT (MAIN MENU LOOP)
# =====================================================================

def display_main_menu():
    """
    Prints the user-friendly command selection menu interface.
    """
    print("\n" + "="*50)
    print("      GEN-Z SOCIAL MEDIA PLANNER & ANALYTICS")
    print("="*50)
    print("  1. Add a New Post Idea")
    print("  2. Update Planned Post Status (Draft -> Sched -> Posted)")
    print("  3. Record Metric Engagement")
    print("  4. View Scheduled Content Calendar")
    print("  5. Generate & Export Performance Report")
    print("  6. Exit Program Session")
    print("="*50)


def main():
    """
    Program execution driver method.
    """
    # Verify file foundations are in place
    initialize_database()

    while True:
        display_main_menu()
        user_choice = input("Enter option number (1-6): ").strip()

        if user_choice == "1":
            add_new_post()
        elif user_choice == "2":
            update_post_status()
        elif user_choice == "3":
            record_engagement()
        elif user_choice == "4":
            display_content_calendar()
        elif user_choice == "5":
            generate_and_export_report()
        elif user_choice == "6":
            print("\n[System Shutdown] Finalizing planning assets...")
            print("Session closed. Good luck with your social media branding channels!")
            break
        else:
            print("[Menu Error] Invalid input selection. Please choose an option between 1 and 6.")


if __name__ == "__main__":
    main()
