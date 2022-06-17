var popup = document.getElementById("popup");

function popupM(name, salt, coast, count, id) {
  popup.style.display = popup.style.display == 'none' ? 'flex' : 'none';
  document.getElementById("name").innerText = name;
  document.getElementById("salt").innerText = salt;
  document.getElementById("price").value = coast;
  document.getElementById("count").value = count;
  document.getElementById("id").value = id;
  document.getElementById("deleteLiq").href = `/admin/del/${id}`;
}

document.getElementById("cancel").addEventListener("click", popupM);
