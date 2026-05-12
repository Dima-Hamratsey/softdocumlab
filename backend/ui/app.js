const API_BASE = "";

const statusLabels = {
  new: "Нове",
  in_review: "На перевірці",
  confirmed: "Підтверджено",
  archived: "Архів",
};

const state = {
  studies: [],
  currentPage: 1,
  pageSize: 100,
  totalCount: 0,
  editingId: null,
};

const elements = {
  addStudyBtn: document.getElementById("addStudyBtn"),
  modal: document.getElementById("studyModal"),
  modalTitle: document.getElementById("modalTitle"),
  closeModal: document.getElementById("closeModal"),
  cancelModal: document.getElementById("cancelModal"),
  form: document.getElementById("studyForm"),
  saveBtn: document.getElementById("saveBtn"),
  prevPageBtn: document.getElementById("prevPageBtn"),
  nextPageBtn: document.getElementById("nextPageBtn"),
  pageInfo: document.getElementById("pageInfo"),
  rangeInfo: document.getElementById("rangeInfo"),
  tableBody: document.getElementById("studiesBody"),
  emptyState: document.getElementById("emptyState"),
  studyCount: document.getElementById("studyCount"),
};

function setModalOpen(isOpen) {
  elements.modal.classList.toggle("hidden", !isOpen);
  elements.modal.setAttribute("aria-hidden", String(!isOpen));
}

function resetForm() {
  elements.form.reset();
  elements.form.status.value = "new";
}

function openModal(mode, study) {
  state.editingId = mode === "edit" && study ? study.id : null;
  elements.modalTitle.textContent =
    mode === "edit" ? "Редагувати запис" : "Додати запис";

  if (study) {
    elements.form.patient_first_name.value = study.patient_first_name || "";
    elements.form.patient_last_name.value = study.patient_last_name || "";
    elements.form.patient_email.value = study.patient_email || "";
    elements.form.doctor_name.value = study.doctor_name || "";
    elements.form.specialization.value = study.specialization || "";
    elements.form.status.value = study.status || "new";
    elements.form.report_text.value = study.report_text || "";
    elements.form.study_file_name.value = study.study_file_name || "";
  } else {
    resetForm();
  }

  setModalOpen(true);
}

function closeModal() {
  setModalOpen(false);
  state.editingId = null;
}

function mapStatus(status) {
  return statusLabels[status] || status;
}

function createCell(text) {
  const cell = document.createElement("td");
  cell.textContent = text;
  return cell;
}

function renderTable(studies) {
  elements.tableBody.innerHTML = "";
  if (!studies.length) {
    elements.emptyState.hidden = false;
    elements.studyCount.textContent = "0 записів";
    return;
  }

  elements.emptyState.hidden = true;
  elements.studyCount.textContent = `${state.totalCount} записів`;

  studies.forEach((study) => {
    const row = document.createElement("tr");
    const patientName = `${study.patient_first_name || ""} ${
      study.patient_last_name || ""
    }`.trim();

    row.appendChild(createCell(study.id));
    row.appendChild(createCell(patientName || "—"));
    row.appendChild(createCell(study.patient_email || "—"));
    row.appendChild(createCell(study.doctor_name));
    row.appendChild(createCell(study.specialization));

    const statusCell = document.createElement("td");
    const badge = document.createElement("span");
    badge.className = `status status-${study.status}`;
    badge.textContent = mapStatus(study.status);
    statusCell.appendChild(badge);
    row.appendChild(statusCell);

    row.appendChild(createCell(study.study_file_name));

    const actionsCell = document.createElement("td");
    actionsCell.className = "actions";

    const editBtn = document.createElement("button");
    editBtn.className = "btn btn-ghost";
    editBtn.textContent = "Редагувати";
    editBtn.dataset.action = "edit";
    editBtn.dataset.id = study.id;

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "btn btn-danger";
    deleteBtn.textContent = "Видалити";
    deleteBtn.dataset.action = "delete";
    deleteBtn.dataset.id = study.id;

    actionsCell.append(editBtn, deleteBtn);
    row.appendChild(actionsCell);

    elements.tableBody.appendChild(row);
  });
}

function clampPage() {
  const totalPages = Math.max(1, Math.ceil(state.totalCount / state.pageSize));
  if (state.currentPage > totalPages) {
    state.currentPage = totalPages;
  }
  if (state.currentPage < 1) {
    state.currentPage = 1;
  }
  return totalPages;
}

function updatePaginationInfo() {
  const totalPages = clampPage();
  const start = state.totalCount
    ? (state.currentPage - 1) * state.pageSize + 1
    : 0;
  const end = Math.min(state.currentPage * state.pageSize, state.totalCount);

  elements.rangeInfo.textContent = `${start}-${end} з ${state.totalCount}`;
  elements.pageInfo.textContent = `Сторінка ${state.currentPage} з ${totalPages}`;
  elements.prevPageBtn.disabled = state.currentPage <= 1;
  elements.nextPageBtn.disabled = state.currentPage >= totalPages;
}

async function fetchJson(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    let message = "Помилка сервера";
    try {
      const payload = await response.json();
      message = payload.detail || message;
    } catch (err) {
      // ignore parsing errors
    }
    throw new Error(message);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

async function loadCounts() {
  const result = await fetchJson("/studies/count");
  state.totalCount = result.count || 0;
  clampPage();
}

async function loadStudies() {
  try {
    const offset = (state.currentPage - 1) * state.pageSize;
    const studies = await fetchJson(
      `/studies?limit=${state.pageSize}&offset=${offset}`
    );
    state.studies = studies;
    renderTable(studies);
    updatePaginationInfo();
  } catch (error) {
    alert(error.message);
  }
}

async function refreshList() {
  await loadCounts();
  await loadStudies();
}

async function saveStudy(event) {
  event.preventDefault();
  const formData = new FormData(elements.form);
  const payload = {
    patient_first_name: formData.get("patient_first_name").trim(),
    patient_last_name: formData.get("patient_last_name").trim(),
    patient_email: formData.get("patient_email").trim(),
    doctor_name: formData.get("doctor_name").trim(),
    specialization: formData.get("specialization").trim(),
    status: formData.get("status"),
    report_text: formData.get("report_text").trim(),
    study_file_name: formData.get("study_file_name").trim(),
  };

  const options = {
    method: state.editingId ? "PUT" : "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  };

  const endpoint = state.editingId
    ? `/studies/${state.editingId}`
    : "/studies";

  elements.saveBtn.disabled = true;
  try {
    await fetchJson(endpoint, options);
    closeModal();
    await refreshList();
  } catch (error) {
    alert(error.message);
  } finally {
    elements.saveBtn.disabled = false;
  }
}

async function deleteStudy(id) {
  const confirmed = confirm("Видалити запис?");
  if (!confirmed) {
    return;
  }

  try {
    await fetchJson(`/studies/${id}`, { method: "DELETE" });
    await refreshList();
  } catch (error) {
    alert(error.message);
  }
}

function handleTableClick(event) {
  const button = event.target.closest("button[data-action]");
  if (!button) {
    return;
  }
  const id = Number(button.dataset.id);
  const action = button.dataset.action;
  const study = state.studies.find((item) => item.id === id);

  if (action === "edit" && study) {
    openModal("edit", study);
  }

  if (action === "delete") {
    deleteStudy(id);
  }
}

elements.addStudyBtn.addEventListener("click", () => openModal("create"));
elements.closeModal.addEventListener("click", closeModal);
elements.cancelModal.addEventListener("click", closeModal);
elements.form.addEventListener("submit", saveStudy);
elements.tableBody.addEventListener("click", handleTableClick);

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !elements.modal.classList.contains("hidden")) {
    closeModal();
  }
});

elements.prevPageBtn.addEventListener("click", async () => {
  if (state.currentPage > 1) {
    state.currentPage -= 1;
    await loadStudies();
  }
});

elements.nextPageBtn.addEventListener("click", async () => {
  const totalPages = Math.max(1, Math.ceil(state.totalCount / state.pageSize));
  if (state.currentPage < totalPages) {
    state.currentPage += 1;
    await loadStudies();
  }
});

async function init() {
  try {
    await refreshList();
  } catch (error) {
    alert(error.message);
  }
}

init();
