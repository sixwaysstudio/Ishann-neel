# 📸 Ishaan Neel Photography Portfolio

A beautiful photography portfolio website with **ultra-fast image loading**.

---

## 🚀 How to Add New Photos

### Option 1: Using GitHub Web (Easiest)

1. Go to your repository on [github.com](https://github.com)
2. Navigate to `assets/images/works/[CATEGORY]/`
   - Categories: `Concerts`, `STREET`, `WILD LIFE`, `LANDSCAPE`, `EXHIBITION`
3. Click **"Add file"** → **"Upload files"**
4. Drag and drop your `.webp`, `.jpg`, or `.png` images
5. Click **"Commit changes"**

**That's it!** Wait 1-2 minutes and your website will automatically update.

### Option 2: Using GitHub Desktop

1. Open GitHub Desktop
2. Add your images to `assets/images/works/[CATEGORY]/`
3. Write a commit message and click **"Commit"**
4. Click **"Push origin"**

---

## 🎨 Image Guidelines

- **Format**: WebP recommended (smallest size), JPEG/PNG also work
- **Size**: Keep images under 2MB for fast loading
- **Naming**: Avoid special characters in filenames

---

## ⚡ What Happens Automatically

When you upload images, GitHub Actions will:

1. ✅ Generate tiny blurred thumbnails (for instant loading)
2. ✅ Update the gallery data
3. ✅ Deploy your website

You don't need to do anything else!

---

## 📁 Folder Structure

```
assets/images/works/
├── Concerts/          # Concert photos
│   ├── Kaaktaal/
│   ├── Metrical/
│   └── ...
├── STREET/            # Street photography
├── WILD LIFE/         # Wildlife photos
├── LANDSCAPE/         # Landscape shots
└── EXHIBITION/        # Exhibition photos
```

---

## 🛠️ Technical Details (For Reference)

- **Hosting**: GitHub Pages (free)
- **Image Optimization**: Automatic thumbnail generation via GitHub Actions
- **Loading**: Progressive blur-to-sharp effect
- **Technology**: HTML, CSS, JavaScript (no frameworks)

---

Made with ❤️
