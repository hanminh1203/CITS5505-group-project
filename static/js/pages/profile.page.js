import { httpService } from '../services/http.service.js';

// Retrieve CSRF token from the meta tag
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

// ─── MODALS ───
// Attach functions to window so they can be called from inline HTML onclick attributes
window.openModal = function(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.add('open');
};

window.closeModal = function(id) {
  const modal = document.getElementById(id);
  if (!modal) return;
  modal.classList.remove('open');
};

// Close modal when clicking outside of it
document.querySelectorAll('.ss-modal-overlay').forEach(o => {
  o.addEventListener('click', function (e) { if (e.target === o) o.classList.remove('open'); });
});

window.openEditProfileModal = function() { window.openModal('modal-edit-profile'); };
window.saveProfile = function() {
  window.closeModal('modal-edit-profile');
  window.showToast('Profile updated!', 'Your changes have been saved.');
};

// ─── SKILL CRUD ───
let editingSkillId = null;

// Open modal to add a new skill
window.openAddSkillModal = function() {
  editingSkillId = null;
  document.getElementById('add-skill-title').textContent = 'Add a Skill';
  document.getElementById('add-skill-sub').textContent = 'Add to your profile so others can find you.';
  document.getElementById('new-skill-name').value = '';
  document.getElementById('new-skill-desc').value = '';
  document.getElementById('new-skill-level').value = 'Beginner'; // Reset dropdown to default
  
  const submitBtn = document.querySelector('#modal-add-skill .btn-accent');
  if (submitBtn) submitBtn.textContent = 'Add Skill';
  
  window.openModal('modal-add-skill');
};

// Save (Create or Update) a skill
window.saveSkill = async function() {
  const name = document.getElementById('new-skill-name').value.trim();
  const desc = document.getElementById('new-skill-desc').value.trim();
  const level = document.getElementById('new-skill-level').value;

  // Basic frontend validation
  if (!name) { 
    window.showToast('Required', 'Please enter a skill name.'); 
    return; 
  }

  try {
    if (editingSkillId) {
      // Update existing skill via API
      await httpService.post(csrfToken, `/api/skills/${editingSkillId}`, { name, description: desc, level });
      window.showToast('Skill updated!', `"${name}" has been updated.`);
    } else {
      // Add new skill via API
      await httpService.post(csrfToken, `/api/skills/`, { name, description: desc, level });
      window.showToast('Skill added!', `"${name}" has been added to your profile.`);
    }
    
    window.closeModal('modal-add-skill');
    // Refresh the page after a short delay to let the user see the success toast
    setTimeout(() => location.reload(), 800);
  } catch (error) {
    console.error("Failed to save skill", error);
    window.showToast('Error', 'Failed to save skill. Please try again.');
  }
};

// Open modal to edit an existing skill
window.editSkill = function(btn) {
  // Find the parent row and extract existing skill data
  const row = btn.closest('.skill-row');
  const skillId = row.getAttribute('data-skill-id');
  const name = row.querySelector('.skill-name').textContent;
  const desc = row.querySelector('.skill-meta').textContent.replace('No description', '').trim();
  const level = row.querySelector('.skill-level').textContent;

  editingSkillId = skillId; // Set the global tracking ID

  // Update modal UI for editing
  document.getElementById('add-skill-title').textContent = 'Edit Skill';
  document.getElementById('add-skill-sub').textContent = 'Update the skill details on your profile.';
  
  const submitBtn = document.querySelector('#modal-add-skill .btn-accent');
  if (submitBtn) submitBtn.textContent = 'Save Changes';

  // Pre-fill form fields
  document.getElementById('new-skill-name').value = name;
  document.getElementById('new-skill-desc').value = desc;
  document.getElementById('new-skill-level').value = level;
  
  window.openModal('modal-add-skill');
};

// Delete an existing skill
window.deleteSkill = async function(btn) {
  const row = btn.closest('.skill-row');
  const skillId = row.getAttribute('data-skill-id');
  const name = row.querySelector('.skill-name').textContent;
  
  if (confirm(`Are you sure you want to remove "${name}" from your profile?`)) {
    try {
      // Delete skill via API
      await httpService.post(csrfToken, `/api/skills/${skillId}/delete`, {});
      
      // Animate removal and refresh
      row.style.opacity = '0';
      row.style.transition = 'opacity 0.3s';
      setTimeout(() => location.reload(), 300);
      
      window.showToast('Skill removed', `"${name}" has been removed.`);
    } catch (error) {
      console.error("Failed to delete skill", error);
      window.showToast('Error', 'Failed to delete skill. Please try again.');
    }
  }
};

// ─── TOAST ───
// Helper function to display toast notifications
window.showToast = function(title, msg) {
  const t = document.getElementById('toast');
  const titleEl = document.getElementById('toast-title');
  const msgEl = document.getElementById('toast-msg');

  if (!t || !titleEl || !msgEl) return;

  titleEl.textContent = title;
  msgEl.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3500);
};