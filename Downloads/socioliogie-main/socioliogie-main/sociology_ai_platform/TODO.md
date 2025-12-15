# TODO: Enhance Forum for File Uploads and Social Interactions

## Steps to Complete

- [ ] Modify social/models.py: Add file field to Post model for PDF, DOC, DOCX, images
- [ ] Update social/views.py: Modify create_post view to handle file upload
- [ ] Edit templates/social/create_post.html: Add file input field
- [ ] Edit templates/social/forum.html: Display file indicator/icon if file attached
- [ ] Edit templates/social/post_detail.html: Display file download link or preview
- [ ] Create and apply database migration for new file field
- [ ] Test file uploads and downloads
- [ ] Restrict file types if necessary (optional)
