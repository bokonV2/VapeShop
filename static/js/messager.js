$(function() {
  window.scrollTo(0, document.body.scrollHeight);

  var channel = document.location.pathname.split('/').at(-1);
  var socket = io();

  socket.emit('join', {
    'channel': channel
  });

  socket.on('Mget', data => {
    console.log(data)
    if (data["me"] != data["channel"]) {
      $(".Cmessager").append(`
        <div class="message__item Mleft">
        <span class="message Mme">${data["mess"]}</span>
        <time class="message MtL">${data["time"]}</time>
        </div>
        `)
    } else {
      $(".Cmessager").append(`
      <div class="message__item Mright">
        <span class="message Mto">${data["mess"]}</span>
        <time class="message MtR">${data["time"]}</time>
      </div>
      `)
    }
    window.scrollTo(0, document.body.scrollHeight + 200);
  });

  $("form").submit(function() {
    var dt = new Date();
    var time = dt.getHours() + ":" + dt.getMinutes();
    var $form = $(this);
    socket.emit('Msend', {
      message: $form.find('input[name=mess]').val(),
      id: channel
    });
    $("#chat-input").val("");
    return false;
  });
});
