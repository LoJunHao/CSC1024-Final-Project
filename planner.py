import os
from datetime import datetime

# Define filenames for the persistent data files
POSTS_FILE = "posts.txt"
PLATFORMS_FILE = "platforms.txt"
ENGAGEMENT_FILE = "engagement.txt"


# ==========================================
# FILE HANDLING & DATA LOADING FUNCTIONS
# ==========================================

def load_platforms():
    """
    Reads platforms.txt and returns a list of dictionaries.
    Fields: Platform ID|Platform Name|Follower Count
    """
    platforms = []
    if not os.path.exists(PLATFORMS_FILE):
        # Create a default file if it does not exist
        f = open(PLATFORMS_FILE, 'w')
        f.write("P1|Instagram|12500\n")
        f.write("P2|TikTok|45000\n")
        f.write("P3|X|8200\n")
        f.close()
    
    f = open(PLATFORMS_FILE, 'r')
    for line in f:
        line = line.strip()
        if line == "":
            continue
        parts = line.split('|')
        if len(parts) == 3:
            platform_dict = {
                "platform_id": parts[0],
                "name": parts[1],
                "followers": int(parts[2])
            }
            platforms.append(platform_dict)
    f.close()
    return platforms


def load_posts():
    """
    Reads posts.txt and returns a list of dictionaries.
    Fields: Post ID|Platform Name|Content Caption|Scheduled Date|Status
    """
    posts = []
    if not os.path.exists(POSTS_FILE):
        return posts
        
    f = open(POSTS_FILE, 'r')
    for line in f:
        line = line.strip()
        if line == "":
            continue
        parts = line.split('|')
        if len(parts) == 5:
            post_dict = {
                "post_id": parts[0],
                "platform": parts[1],
                "caption": parts[2],
                "date": parts[3],
                "status": parts[4]
            }
            posts.append(post_dict)
    f.close()
    return posts


def save_posts(posts):
    """
    Writes the list of post dictionaries back to posts.txt.
    """
    f = open(POSTS_FILE, 'w')
    for post in posts:
        line = post['post_id'] + "|" + post['platform'] + "|" + post['caption'] + "|" + post['date'] + "|" + post['status'] + "\n"
        f.write(line)
    f.close()


def load_engagement():
    """
    Reads engagement.txt and returns a list of dictionaries.
    Fields: Post ID|Likes|Comments|Shares|Views
    """
    engagement = []
    if not os.path.exists(ENGAGEMENT_FILE):
        return engagement
        
    f = open(ENGAGEMENT_FILE, 'r')
    for line in f:
        line = line.strip()
        if line == "":
            continue
        parts = line.split('|')
        if len(parts) == 5:
            eng_dict = {
                "post_id": parts[0],
                "likes": int(parts[1]),
                "comments": int(parts[2]),
                "shares": int(parts[3]),
                "views": int(parts[4])
            }
            engagement.append(eng_dict)
    f.close()
    return engagement


def save_engagement(engagement_list):
    """
    Writes the list of engagement dictionaries back to engagement.txt.
    """
    f = open(ENGAGEMENT_FILE, 'w')
    for eng in engagement_list:
        line = eng['post_id'] + "|" + str(eng['likes']) + "|" + str(eng['comments']) + "|" + str(eng['shares']) + "|" + str(eng['views']) + "\n"
        f.write(line)
    f.close()


# ==========================================
# VALIDATION HELPER FUNCTIONS
# ==========================================

def get_valid_date(prompt):
    """
    Prompts the user for a date in YYYY-MM-DD format and validates it.
    Loops until a valid date is entered or the user types 'cancel'.
    """
    while True:
        date_input = input(prompt).strip()
        if date_input.lower() == 'cancel':
            return None
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("[ERROR] Invalid date format! Please enter a valid date in YYYY-MM-DD format (or type 'cancel' to abort).")


def get_non_negative_int(prompt):
    """
    Prompts the user for a non-negative integer and validates it.
    Loops until a valid number is entered.
    """
    while True:
        num_input = input(prompt).strip()
        if num_input.isdigit():
            return int(num_input)
        else:
            print("[ERROR] Please enter a valid non-negative integer (e.g., 0, 100, 500).")


# ==========================================
# CORE FEATURES / OPTIONS
# ==========================================

def add_new_post_idea():
    """
    Option 1: Add a new post idea.
    Guides the user to enter fields and validates data.
    """
    print("\n========================================")
    print("      ADD NEW POST IDEA")
    print("========================================")

    platforms = load_platforms()
    posts = load_posts()

    # Get unique Post ID
    while True:
        post_id = input("Enter Post ID (e.g., POST005, or 'cancel' to exit): ").strip()
        if post_id.lower() == 'cancel':
            print("Action cancelled. Returning to main menu...")
            return
        if post_id == "":
            print("[ERROR] Post ID cannot be empty.")
            continue
        
        # Check if Post ID already exists
        exists = False
        for post in posts:
            if post["post_id"].lower() == post_id.lower():
                exists = True
                break
        
        if exists:
            print("[ERROR] Post ID '" + post_id + "' already exists. Please choose a unique ID.")
        else:
            break

    # Get platform name
    valid_platforms = []
    for p in platforms:
        valid_platforms.append(p["name"])
        
    print("Available Platforms: " + ", ".join(valid_platforms))
    while True:
        platform_choice = input("Enter target platform: ").strip()
        match = None
        for p in valid_platforms:
            if p.lower() == platform_choice.lower():
                match = p
                break
        
        if match != None:
            platform_name = match
            break
        else:
            print("[ERROR] Invalid platform. Please choose from: " + ", ".join(valid_platforms))

    # Get content caption
    while True:
        caption = input("Enter content caption: ").strip()
        if caption == "":
            print("[ERROR] Caption cannot be empty.")
            continue
        if "|" in caption:
            print("[ERROR] Caption cannot contain the character '|' because it is used as a data separator.")
            continue
        break

    # Get scheduled date
    scheduled_date = get_valid_date("Enter scheduled date (YYYY-MM-DD): ")
    if scheduled_date is None:
        print("Action cancelled. Returning to main menu...")
        return

    # Add new post as Draft
    new_post = {
        "post_id": post_id,
        "platform": platform_name,
        "caption": caption,
        "date": scheduled_date,
        "status": "Draft"
    }
    posts.append(new_post)
    save_posts(posts)
    print("\n[SUCCESS] Post '" + post_id + "' successfully added as a Draft!")


def update_post_status():
    """
    Option 2: Update post status.
    Allows status updates: Draft -> Scheduled or Scheduled -> Posted.
    """
    print("\n========================================")
    print("      UPDATE POST STATUS")
    print("========================================")

    posts = load_posts()
    if len(posts) == 0:
        print("No posts found. Add a post first!")
        return

    post_id = input("Enter Post ID to update: ").strip()
    
    target_post = None
    for post in posts:
        if post["post_id"].lower() == post_id.lower():
            target_post = post
            break

    if target_post is None:
        print("[ERROR] Post with ID '" + post_id + "' could not be found.")
        return

    current_status = target_post["status"]
    print("Current Status of post '" + target_post['post_id'] + "': " + current_status)

    if current_status.lower() == "draft":
        print("1. Change status to 'Scheduled'")
        print("2. Cancel")
        choice = input("Enter choice (1-2): ").strip()
        if choice == "1":
            target_post["status"] = "Scheduled"
            save_posts(posts)
            print("[SUCCESS] Post status updated to 'Scheduled'.")
        else:
            print("Update cancelled.")

    elif current_status.lower() == "scheduled":
        print("1. Change status to 'Posted'")
        print("2. Change status back to 'Draft'")
        print("3. Cancel")
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            target_post["status"] = "Posted"
            save_posts(posts)
            print("[SUCCESS] Post status updated to 'Posted'.")
        elif choice == "2":
            target_post["status"] = "Draft"
            save_posts(posts)
            print("[SUCCESS] Post status changed back to 'Draft'.")
        else:
            print("Update cancelled.")

    elif current_status.lower() == "posted":
        print("[INFO] This post is already 'Posted'. Status update is not required.")
    else:
        print("[ERROR] Unknown post status: " + current_status)


def record_engagement_metrics():
    """
    Option 3: Record engagement metrics for a posted piece of content.
    """
    print("\n========================================")
    print("    RECORD ENGAGEMENT METRICS")
    print("========================================")

    posts = load_posts()
    post_id = input("Enter Post ID to record engagement: ").strip()

    target_post = None
    for post in posts:
        if post["post_id"].lower() == post_id.lower():
            target_post = post
            break

    if target_post is None:
        print("[ERROR] Post with ID '" + post_id + "' does not exist.")
        return

    if target_post["status"].lower() != "posted":
        print("[ERROR] Cannot log metrics. Post status is '" + target_post['status'] + "'.")
        print("Only posts with 'Posted' status can have engagement metrics.")
        return

    print("Recording engagement for post: " + target_post['caption'][:30] + "...")
    likes = get_non_negative_int("Enter number of Likes: ")
    comments = get_non_negative_int("Enter number of Comments: ")
    shares = get_non_negative_int("Enter number of Shares: ")
    views = get_non_negative_int("Enter number of Views: ")

    engagement_list = load_engagement()
    
    existing_record = None
    for eng in engagement_list:
        if eng["post_id"].lower() == post_id.lower():
            existing_record = eng
            break

    if existing_record != None:
        existing_record["likes"] = likes
        existing_record["comments"] = comments
        existing_record["shares"] = shares
        existing_record["views"] = views
        print("[SUCCESS] Engagement metrics updated for '" + target_post['post_id'] + "'.")
    else:
        new_engagement = {
            "post_id": target_post["post_id"],
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "views": views
        }
        engagement_list.append(new_engagement)
        print("[SUCCESS] Engagement metrics logged for '" + target_post['post_id'] + "'.")

    save_engagement(engagement_list)


def get_post_date(post):
    """Helper function to get post date for sorting without using lambda."""
    return post["date"]


def display_content_calendar():
    """
    Option 4: Display content calendar.
    Shows posts sorted by scheduled date, platform, caption preview, and status.
    """
    print("\n============================================================")
    print("                    CONTENT CALENDAR")
    print("============================================================")

    posts = load_posts()
    if len(posts) == 0:
        print("No scheduled posts to show. Add some post ideas first!")
        return

    # Sort posts by date using a named function instead of lambda
    posts.sort(key=get_post_date)

    print("Post ID    | Scheduled Date  | Platform   | Status     | Caption Preview")
    print("---------------------------------------------------------------------------")

    for post in posts:
        caption = post["caption"]
        if len(caption) > 25:
            preview = caption[:22] + "..."
        else:
            preview = caption

        # Basic string formatting with spacing
        line = post['post_id'] + " " * (10 - len(post['post_id'])) + " | " + \
               post['date'] + " " * (15 - len(post['date'])) + " | " + \
               post['platform'] + " " * (10 - len(post['platform'])) + " | " + \
               post['status'] + " " * (10 - len(post['status'])) + " | " + preview
        print(line)
    print("============================================================")


def delete_post():
    """
    Option 5: Delete a post.
    Implements a cascading delete on engagement.txt.
    """
    print("\n========================================")
    print("           DELETE POST")
    print("========================================")

    posts = load_posts()
    if len(posts) == 0:
        print("No posts available to delete.")
        return

    post_id = input("Enter Post ID to delete: ").strip()

    found_index = -1
    for i in range(len(posts)):
        if posts[i]["post_id"].lower() == post_id.lower():
            found_index = i
            break

    if found_index == -1:
        print("[ERROR] Post ID '" + post_id + "' could not be found.")
        return

    post_to_delete = posts[found_index]
    print("\nAre you sure you want to delete this post?")
    print("ID: " + post_to_delete['post_id'])
    print("Platform: " + post_to_delete['platform'])
    print("Caption: " + post_to_delete['caption'])
    
    confirm = input("Type 'YES' to confirm deletion: ").strip()

    if confirm == "YES":
        deleted_post = posts[found_index]
        del posts[found_index]
        save_posts(posts)
        print("\n[SUCCESS] Post '" + deleted_post['post_id'] + "' has been deleted.")

        # Cascading delete in engagement.txt without list comprehensions
        engagement_list = load_engagement()
        updated_engagement = []
        for eng in engagement_list:
            if eng["post_id"].lower() != post_id.lower():
                updated_engagement.append(eng)
        
        if len(engagement_list) != len(updated_engagement):
            save_engagement(updated_engagement)
            print("[INFO] Corresponding engagement metrics were also deleted to maintain database consistency.")
    else:
        print("Deletion cancelled.")


def compile_performance_report_data():
    """
    Helper function that computes statistics for the performance report.
    """
    platforms = load_platforms()
    posts = load_posts()
    engagement_list = load_engagement()

    # 1. Total posts per platform
    posts_per_platform = {}
    for platform in platforms:
        posts_per_platform[platform["name"]] = 0

    for post in posts:
        p_name = post["platform"]
        if p_name in posts_per_platform:
            posts_per_platform[p_name] = posts_per_platform[p_name] + 1
        else:
            posts_per_platform[p_name] = 1

    # Match posts with engagement for metric analysis
    eng_lookup = {}
    for eng in engagement_list:
        eng_lookup[eng["post_id"].lower()] = eng

    # 2. Find best-performing post
    best_post = None
    max_engagement = -1

    for post in posts:
        pid_lower = post["post_id"].lower()
        if pid_lower in eng_lookup:
            eng = eng_lookup[pid_lower]
            total_eng = eng["likes"] + eng["comments"] + eng["shares"] + eng["views"]
            if total_eng > max_engagement:
                max_engagement = total_eng
                best_post = {
                    "post_id": post["post_id"],
                    "platform": post["platform"],
                    "caption": post["caption"],
                    "total_engagement": total_eng,
                    "likes": eng["likes"],
                    "comments": eng["comments"],
                    "shares": eng["shares"],
                    "views": eng["views"]
                }

    # 3. Find platform with most interaction
    platform_interaction = {}
    for platform in platforms:
        platform_interaction[platform["name"]] = 0

    for post in posts:
        pid_lower = post["post_id"].lower()
        if pid_lower in eng_lookup:
            eng = eng_lookup[pid_lower]
            total_eng = eng["likes"] + eng["comments"] + eng["shares"] + eng["views"]
            p_name = post["platform"]
            if p_name in platform_interaction:
                platform_interaction[p_name] = platform_interaction[p_name] + total_eng
            else:
                platform_interaction[p_name] = total_eng

    # Find the platform with max interaction value (without using dict.items())
    most_interactive_platform = None
    max_platform_interaction = -1
    for p_name in platform_interaction:
        total_int = platform_interaction[p_name]
        if total_int > max_platform_interaction:
            max_platform_interaction = total_int
            most_interactive_platform = p_name

    return {
        "posts_per_platform": posts_per_platform,
        "best_post": best_post,
        "most_interactive_platform": most_interactive_platform,
        "max_platform_interaction": max_platform_interaction
    }


def generate_performance_report():
    """
    Option 6: Generate performance report.
    Displays summary to command-line screen.
    """
    print("\n==================================================")
    print("             PERFORMANCE REPORT SUMMARY")
    print("==================================================")

    report = compile_performance_report_data()

    print("\n--- Total Posts Per Platform ---")
    posts_per_p = report["posts_per_platform"]
    for platform in posts_per_p:
        count = posts_per_p[platform]
        print(" - " + platform + ": " + str(count) + " post(s)")

    print("\n--- Best-Performing Post ---")
    best = report["best_post"]
    if best != None:
        print(" Post ID: " + str(best['post_id']))
        print(" Platform: " + str(best['platform']))
        print(" Caption: \"" + str(best['caption']) + "\"")
        print(" Engagement Breakdown: Likes: " + str(best['likes']) + " | Comments: " + str(best['comments']) + " | Shares: " + str(best['shares']) + " | Views: " + str(best['views']))
        print(" Total Interaction Value: " + str(best['total_engagement']))
    else:
        print(" No posts have engagement metrics logged yet.")

    print("\n--- Platform With Most Interaction ---")
    if report["most_interactive_platform"] != None and report["max_platform_interaction"] > 0:
        print(" Platform: " + str(report['most_interactive_platform']))
        print(" Total Interaction Points: " + str(report['max_platform_interaction']))
    else:
        print(" No platform interactions logged yet.")

    print("\n==================================================")


def export_report_to_file():
    """
    Option 7: Export report to file (e.g. report.txt).
    Saves the performance summary to a text file.
    """
    print("\n========================================")
    print("          EXPORT REPORT TO FILE")
    print("========================================")

    report = compile_performance_report_data()
    export_filename = "report.txt"

    try:
        f = open(export_filename, "w")
        f.write("=============================================\n")
        f.write("      SOCIAL MEDIA PERFORMANCE REPORT\n")
        f.write("      Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("=============================================\n\n")

        f.write("--- Total Posts Per Platform ---\n")
        posts_per_p = report["posts_per_platform"]
        for platform in posts_per_p:
            count = posts_per_p[platform]
            f.write(" - " + platform + ": " + str(count) + " post(s)\n")

        f.write("\n--- Best-Performing Post ---\n")
        best = report["best_post"]
        if best != None:
            f.write(" Post ID: " + str(best['post_id']) + "\n")
            f.write(" Platform: " + str(best['platform']) + "\n")
            f.write(" Caption: \"" + str(best['caption']) + "\"\n")
            f.write(" Engagement Breakdown: Likes: " + str(best['likes']) + " | Comments: " + str(best['comments']) + " | Shares: " + str(best['shares']) + " | Views: " + str(best['views']) + "\n")
            f.write(" Total Interaction Value: " + str(best['total_engagement']) + "\n")
        else:
            f.write(" No posts have engagement metrics logged yet.\n")

        f.write("\n--- Platform With Most Interaction ---\n")
        if report["most_interactive_platform"] != None and report["max_platform_interaction"] > 0:
            f.write(" Platform: " + str(report['most_interactive_platform']) + "\n")
            f.write(" Total Interaction Points: " + str(report['max_platform_interaction']) + "\n")
        else:
            f.write(" No platform interactions logged yet.\n")

        f.write("\n=============================================\n")
        f.close()

        print("[SUCCESS] Performance report successfully exported to '" + export_filename + "'!")
    except Exception as e:
        print("[ERROR] Failed to export report. Reason: " + str(e))


# ==========================================
# MAIN APPLICATION LOOP
# ==========================================

def main():
    """
    Main menu driver function.
    """
    load_platforms()

    while True:
        print("\n=============================================")
        print("    SOCIAL MEDIA CONTENT PLANNER - MAIN MENU")
        print("=============================================")
        print(" 1. Add a New Post Idea")
        print(" 2. Update Post Status")
        print(" 3. Record Engagement Metrics")
        print(" 4. Display Content Calendar")
        print(" 5. Delete a Post Idea (With Cascading Delete)")
        print(" 6. Generate Performance Report")
        print(" 7. Export Performance Report to File")
        print(" 8. Exit")
        print("=============================================")
        
        choice = input("Enter choice (1-8): ").strip()

        if choice == "1":
            add_new_post_idea()
        elif choice == "2":
            update_post_status()
        elif choice == "3":
            record_engagement_metrics()
        elif choice == "4":
            display_content_calendar()
        elif choice == "5":
            delete_post()
        elif choice == "6":
            generate_performance_report()
        elif choice == "7":
            export_report_to_file()
        elif choice == "8":
            print("\nThank you for using the Social Media Content Planner. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
