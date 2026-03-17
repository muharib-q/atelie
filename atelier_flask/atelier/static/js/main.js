// Scroll reveal
const obs = new IntersectionObserver((entries) => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) setTimeout(() => e.target.classList.add('visible'), i * 80);
  });
}, {threshold: 0.08});
document.querySelectorAll('.reveal').forEach(r => obs.observe(r));

// Modal
function openModal(t, d) {
  document.getElementById('modalTitle').textContent = t;
  document.getElementById('modalDesc').textContent = d;
  document.getElementById('modalOverlay').classList.add('active');
}
function closeModal(e) {
  if (!e || e.target === document.getElementById('modalOverlay') || !e.target.closest('.modal'))
    document.getElementById('modalOverlay').classList.remove('active');
}

// Phone mask
const phoneInput = document.getElementById('phone');
if (phoneInput) {
  phoneInput.addEventListener('input', function () {
    let v = this.value.replace(/\D/g, '');
    if (v[0] === '7' || v[0] === '8') v = v.substring(1);
    let r = '+7 (';
    if (v.length > 0) r += v.substring(0, 3);
    if (v.length >= 4) r += ') ' + v.substring(3, 6);
    if (v.length >= 7) r += '-' + v.substring(6, 8);
    if (v.length >= 9) r += '-' + v.substring(8, 10);
    this.value = r;
  });
}

// Nav shrink on scroll
window.addEventListener('scroll', () => {
  document.getElementById('navbar').style.padding =
    window.scrollY > 50 ? '12px 60px' : '18px 60px';
});
