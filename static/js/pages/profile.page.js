// ─── PAGE NAVIGATION ───
  function showPage(id) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-' + id).classList.add('active');
    window.scrollTo(0, 0);
  }

  // ─── AUTH ───
  function doLogin() {
    const email = document.getElementById('login-email').value;
    const pw = document.getElementById('login-pw').value;
    if (!email || !pw) { showToast('Missing fields', 'Please enter your email and password.'); return; }
    showPage('dashboard');
    showToast('Welcome back!', 'Signed in as Alex Chen.');
  }

  function doRegister() {
    showPage('dashboard');
    showToast('Account created!', 'Welcome to SkillSwap, Alex.');
  }

  // ─── MODALS ───
  function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.add('open');
  }

  function closeModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.remove('open');
  }
  document.querySelectorAll('.ss-modal-overlay').forEach(o => {
    o.addEventListener('click', function(e) { if (e.target === o) o.classList.remove('open'); });
  });

  function openOfferModal() { openModal('modal-offer'); }
  function openNewRequestModal() { openModal('modal-new-request'); }
  function openEditProfileModal() { openModal('modal-edit-profile'); }

  let currentSkillType = 'offer';
  let editingSkillRow = null;

  function openAddSkillModal(type) {
    currentSkillType = type;
    editingSkillRow = null;
    document.getElementById('add-skill-title').textContent = type === 'offer' ? 'Add a Skill I Offer' : 'Add a Skill I Want to Learn';
    document.getElementById('add-skill-sub').textContent = type === 'offer' ? 'Add this skill to your offering profile.' : 'Add this to your learning wish list.';
    document.getElementById('new-skill-name').value = '';
    document.getElementById('new-skill-desc').value = '';
    const submitBtn = document.querySelector('#modal-add-skill .btn-accent');
    if (submitBtn) submitBtn.textContent = 'Add Skill';
    openModal('modal-add-skill');
  }

  // ─── SKILL CRUD ───
  function selectLevel(btn) {
    document.querySelectorAll('#level-btns .level-btn').forEach(b => b.classList.remove('sel'));
    btn.classList.add('sel');
  }

  function saveSkill() {
    const name = document.getElementById('new-skill-name').value.trim();
    const desc = document.getElementById('new-skill-desc').value.trim();
    const level = document.querySelector('#level-btns .level-btn.sel')?.textContent || 'Beginner';
    if (!name) { showToast('Required', 'Please enter a skill name.'); return; }

    if (editingSkillRow) {
      const skillNameEl = editingSkillRow.querySelector('.skill-name');
      const skillDescEl = editingSkillRow.querySelector('.skill-meta');
      const skillLevelEl = editingSkillRow.querySelector('.skill-level');
      if (skillNameEl) skillNameEl.textContent = name;
      if (skillDescEl) skillDescEl.textContent = desc || 'No description';
      if (skillLevelEl) skillLevelEl.textContent = level;
    } else {
      const listId = currentSkillType === 'offer' ? 'offer-skills-list' : 'want-skills-list';
      const list = document.getElementById(listId);
      const row = document.createElement('div');
      row.className = 'skill-row';
      row.innerHTML = `
      <div><div class="skill-name">${name}</div><div class="skill-meta" style="font-size:0.78rem;color:var(--muted)">${desc || 'No description'}</div></div>
      <div class="d-flex align-items-center gap-2">
        <span class="skill-level">${level}</span>
        <button class="btn btn-sm" onclick="editSkill(this)" style="color:var(--muted);background:none;border:none;padding:2px 6px;"><i class="bi bi-pencil-fill"></i></button>
        <button class="btn btn-sm" onclick="deleteSkill(this)" style="color:#e05555;background:none;border:none;padding:2px 6px;"><i class="bi bi-trash-fill"></i></button>
      </div>`;
      list.appendChild(row);
    }

    editingSkillRow = null;
    closeModal('modal-add-skill');
    showToast('Skill saved!', `"${name}" has been updated.`);
  }

  function deleteSkill(btn) {
    const row = btn.closest('.skill-row');
    const name = row.querySelector('.skill-name').textContent;
    if (confirm(`Remove "${name}" from your profile?`)) {
      row.style.opacity = '0';
      row.style.transition = 'opacity 0.3s';
      setTimeout(() => row.remove(), 300);
      showToast('Skill removed', `"${name}" has been removed.`);
    }
  }

  function editSkill(btn) {
    const row = btn.closest('.skill-row');
    const name = row.querySelector('.skill-name').textContent;
    const desc = row.querySelector('.skill-meta')?.textContent || row.querySelector('.skill-name')?.nextElementSibling?.textContent || '';
    const level = row.querySelector('.skill-level').textContent;

    editingSkillRow = row;
    currentSkillType = row.closest('#offer-skills-list') ? 'offer' : 'want';

    document.getElementById('add-skill-title').textContent = 'Edit Skill';
    document.getElementById('add-skill-sub').textContent = 'Update the skill details on your profile.';
    const submitBtn = document.querySelector('#modal-add-skill .btn-accent');
    if (submitBtn) submitBtn.textContent = 'Save Changes';

    document.getElementById('new-skill-name').value = name;
    document.getElementById('new-skill-desc').value = desc === 'No description' ? '' : desc;
    document.querySelectorAll('#level-btns .level-btn').forEach(b => {
      b.classList.toggle('sel', b.textContent === level);
    });
    openModal('modal-add-skill');
  }

  // ─── OTHER ACTIONS ───
  function submitOffer() {
    closeModal('modal-offer');
    showToast('Offer sent!', 'Alex will be notified of your offer.');
  }

  function createRequest() {
    closeModal('modal-new-request');
    showToast('Request posted!', 'Your request is now live on SkillSwap.');
  }

  function saveProfile() {
    closeModal('modal-edit-profile');
    showToast('Profile updated!', 'Your changes have been saved.');
  }

  function acceptOffer(btn) {
    const offerCard = btn.closest('.offer-card');
    const user = offerCard.querySelector('.offer-user').textContent;
    if (confirm(`Accept offer from ${user}? This will close the request to new offers.`)) {
      // Update badge
      const badge = document.querySelector('.detail-hero .badge-status');
      if (badge) { badge.className = 'badge-status badge-accepted'; badge.textContent = 'Accepted'; }
      // Disable other accept buttons
      document.querySelectorAll('.offer-card .btn-accent').forEach(b => {
        b.disabled = true; b.textContent = 'Accepted'; b.style.opacity = '0.5';
      });
      btn.disabled = false; btn.textContent = '✓ Accepted'; btn.style.opacity = '1';
      showToast('Offer accepted!', `You've accepted ${user}'s offer. Happy swapping!`);
    }
  }

  function toggleChip(el) {
    document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
  }

  // ─── TOAST ───
  function showToast(title, msg) {
    const t = document.getElementById('toast');
    const titleEl = document.getElementById('toast-title');
    const msgEl = document.getElementById('toast-msg');

    if (!t || !titleEl || !msgEl) {
      return;
    }

    titleEl.textContent = title;
    msgEl.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3500);
  }