# app.py
import json
from agent import WebDevAgent


def main():
    agent = WebDevAgent()

    user_prompt = input("Enter your website prompt: ").strip()

    raw_assets = input("Enter asset paths as JSON list (or press Enter): ").strip()
    asset_paths = []
    if raw_assets:
        try:
            asset_paths = json.loads(raw_assets)
        except Exception:
            print('Invalid JSON list. Example: ["./a.png", "./b.mp4"]')
            asset_paths = []

    final_state = agent.run(user_prompt, asset_paths)
    print("\n--- FINAL RESPONSE ---")
    print(final_state.final_response)





from agent import WebDevAgent

if __name__ == "__main__":
    agent = WebDevAgent()

    user_prompt = """
Build a clean, modern, mobile-first single-page e-commerce landing site for a premium tech store called “NovaStore”.

Theme / UI:
- Minimal, premium look (Apple-style)
- Light theme with subtle gradients and a single accent color
- Smooth micro-interactions (hover, focus, scroll-in animations)
- Very clean typography and spacing, responsive grid

Sections (single page):
1) Header:
   - Brand: NovaStore
   - Nav anchors: Home, Products, Deals, FAQ, Contact
   - Add a cart button/icon in header (front-end only)
   - Add a search input (front-end only; filtering can be basic in JS)

2) Hero:
   - Headline: “Upgrade your everyday.”
   - Subtext: premium devices, fast shipping, easy returns
   - Primary CTA: “Shop Products” (scroll to Products)
   - Secondary CTA: “View Deals” (scroll to Deals)

3) Products grid (core):
   - Build a product grid with 3 featured products using ONLY the provided images:
     A) Apple Watch (image asset)
     B) iPad A16 (image asset)
     C) MacBook Air M4 (image asset)
   - Each product card must include:
     - product image
     - name + short 1-line description
     - price (reasonable values)
     - rating clarifier (e.g., ★★★★☆ 4.6)
     - “Add to Cart” button (updates a cart count in header)
     - “Quick View” button that opens a modal showing the larger image + key specs

4) Deals section:
   - Show 2–3 deal banners/cards (e.g., “Student Discount”, “Bundle & Save”)
   - Add “Apply Deal” buttons (front-end only; show toast or message)

5) FAQ:
   - Create an accordion with 5 questions:
     shipping, returns, warranty, payment, support

6) Contact:
   - Simple contact form (name/email/message)
   - Add support hours (don’t invent address; keep it generic)

Interactivity (JS):
- Smooth scrolling for nav links
- Product search filter (filter by product name)
- Add-to-cart updates a cart count badge
- Quick View modal (re-use your existing modal pattern)
- FAQ accordion toggle
- Scroll-in animation using IntersectionObserver (optional)

Assets:
- Use ONLY the assets I provide via ASSETS_MANIFEST_JSON.site_rel_path.
- Do not invent any other images/icons. If needed, use simple inline SVGs or pure CSS shapes.
- Product images must come from the given 3 files.

Output:
- Generate index.html, styles.css, app.js (no markdown fences).
"""

    asset_paths = [
        "/Users/manikantamb/Downloads/Site_Demos/_3_Apple_Watch.jpg",
        "/Users/manikantamb/Downloads/Site_Demos/_3_IPad_A16.jpg",
        "/Users/manikantamb/Downloads/Site_Demos/_3_MacBook_Air_M4.jpg",
    ]

    final_state = agent.run(user_prompt=user_prompt, asset_paths=asset_paths)

    print("\n--- FINAL RESPONSE ---")
    print(final_state.final_response)

# # my cafe creation example
# if __name__ == "__main__":
#     agent = WebDevAgent()

#     user_prompt = """
# Build a clean, modern, mobile-first café website (single-page) for “Manis Cafe”.

# Theme:
# - Warm, cozy, premium coffee aesthetic
# - Dark mode base with a coffee/brown accent color
# - Smooth subtle animations (hover, fade-in on scroll)

# Sections (single page):
# 1) Header + Nav (anchors): Home, Menu, About, Gallery, Reviews, Contact
# 2) Hero:
#    - Café name “Manis Cafe”
#    - Short tagline: “Fresh brews, warm vibes.”
#    - Primary CTA button: “View Menu” (scroll to Menu)
#    - Secondary CTA: “Find Us” (scroll to Contact)
#    - Use the logo image in the header and/or hero
# 3) Menu:
#    - Create 3 categories with cards:
#      - Coffee (Espresso, Cappuccino, Latte, Cold Brew)
#      - Snacks (Croissant, Sandwich, Muffin)
#      - Desserts (Cheesecake, Brownie, Tiramisu)
#    - Add short descriptions + prices (reasonable values)
# 4) About:
#    - Short story of the café (2–3 paragraphs)
#    - Highlight: ethically sourced beans, handcrafted drinks, calm workspace
# 5) Gallery:
#    - Show a responsive image grid using the provided coffee images
# 6) Reviews:
#    - 3–4 testimonial cards (realistic names + short quotes)
# 7) Contact:
#    - Address, hours, phone (do not invent email if not provided)
#    - Simple contact form: name/email/message (front-end only)
#    - Add a “Get Directions” button that opens Google Maps using a placeholder link (no exact location)

# Assets rules:
# - Use ONLY the assets I provide (exact paths copied into the manifest).
# - Place them properly: logo in header, photos in hero/gallery.
# - Do not reference any other images.

# Output:
# - Generate index.html, styles.css, app.js
# - Include smooth scrolling and scroll-in animations.
# """

#     asset_paths = [
#         "/Users/manikantamb/Downloads/Site_Demos/_2_Manis Cafe_logo.png",
#         "/Users/manikantamb/Downloads/Site_Demos/_2_coffee_demo_pic1.jpg",
#         "/Users/manikantamb/Downloads/Site_Demos/_2_coffee_demo_pic3.png",
#         "/Users/manikantamb/Downloads/Site_Demos/_2_coffee_demo_pic4.png",
#         "/Users/manikantamb/Downloads/Site_Demos/_2_Coffee_seeds_demo_pic2.jpg",
#     ]

#     final_state = agent.run(user_prompt=user_prompt, asset_paths=asset_paths)

#     print("\n--- FINAL RESPONSE ---")
#     print(final_state.final_response)
