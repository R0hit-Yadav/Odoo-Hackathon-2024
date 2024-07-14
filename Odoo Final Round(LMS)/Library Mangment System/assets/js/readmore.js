const readMoreBtn = document.querySelector('.read-more-btn');
const hiddenContent = document.querySelector('.hidden-content');

readMoreBtn.addEventListener('click', () => {
  hiddenContent.style.display = hiddenContent.style.display === 'none' ? 'block' : 'none';
  readMoreBtn.textContent = readMoreBtn.textContent === 'Read More' ? 'Read Less' : 'Read More';
});
