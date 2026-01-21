const fs = require('fs');
const path = require('path');

// Configuration
const WORKS_DIR = path.join(__dirname, '../assets/images/works');
const OUTPUT_FILE = path.join(__dirname, '../assets/js/gallery-data.js');

// Helper to get all files recursively
const getImages = (dir, category = '') => {
    let results = [];
    const list = fs.readdirSync(dir);

    list.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat && stat.isDirectory()) {
            // Skip thumbs directories
            if (file === 'thumbs') return;

            const newCategory = category || file;
            results = results.concat(getImages(filePath, newCategory));
        } else {
            if (/\.(webp|jpg|jpeg|png|gif)$/i.test(file)) {
                const relativePath = path.relative(WORKS_DIR, filePath).replace(/\\/g, '/');
                const pathParts = relativePath.split('/');

                // Top level folder is the Category
                const mainCategory = pathParts[0];

                // Generate a title from the filename
                const title = path.basename(file, path.extname(file)).replace(/[_-]/g, ' ');

                results.push({
                    src: `../assets/images/works/${encodeURI(relativePath)}`,
                    category: mainCategory.toLowerCase(),
                    title: title,
                    originalCategory: mainCategory
                });
            }
        }
    });
    return results;
};

try {
    console.log('Scanning images...');
    const images = getImages(WORKS_DIR);

    const fileContent = `// Auto-generated gallery data
const galleryData = ${JSON.stringify(images, null, 4)};
`;

    fs.writeFileSync(OUTPUT_FILE, fileContent);
    console.log(`Success! Found ${images.length} images.`);
    console.log(`Data saved to: ${OUTPUT_FILE}`);
} catch (err) {
    console.error('Error generating gallery data:', err);
}
