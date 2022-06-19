var popup = document.getElementById("popup");

function popupM(fio, name, salt, count, coast, id) {
  popup.style.display = popup.style.display == 'none' ? 'flex' : 'none';
  document.getElementById("fio").innerText = fio;
  document.getElementById("name").innerText = name;
  document.getElementById("salt").innerText = salt;
  document.getElementById("price").innerText = `${coast}р`;
  document.getElementById("count").innerText = `${count}+1 штук`;
  document.getElementById("accept").href = `/qur/${id}/1`;
  document.getElementById("cancle").href = `/qur/${id}/0`;
  ""
}

document.getElementById("cancel").addEventListener("click", popupM);
