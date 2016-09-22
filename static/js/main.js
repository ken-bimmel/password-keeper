var rh = rh || {};
rh.pk = rh.pk || {};

rh.pk.mdlInitializations = function() {
  // Polyfill for browsers that don't support the dialog tag.
  var dialogs = document.querySelectorAll('dialog');
  for (var i = 0; i < dialogs.length; i++) {
    // Using an old school style for loop since this for compatibility.
    var dialog = dialogs[i];
    if (!dialog.showModal) {
      dialogPolyfill.registerDialog(dialog);
    }
  }
};

rh.pk.enableButtons = function() {

  // Collapse or expand password cards.
  $(".password-card .mdl-card__title").click(function() {
    var $header = $(this)
    var $content = $header.next();
    $content.slideToggle(250, function() {
      if ($content.is(":visible")) {
        $header.find(".edit-password-btn").show();
      } else {
        $header.find(".edit-password-btn").hide();
      }
    });
  });

  // Add a new password
  $("#add-password-fab").click(function() {
    console.log("Add password click");
    document.querySelector('#insert-password-dialog').showModal();

    $("#insert-password-dialog input[name=password_entity_key]").val("");
    $("#insert-password-dialog input[name=service]").val("");
    $("#insert-password-dialog input[name=username]").val("");
    $("#insert-password-dialog input[name=password]").val("");
    $("#insert-password-dialog .service-for-delete").val("");
    $("#insert-password-dialog .entity-key-for-delete").val("");
    $("#insert-password-dialog .mdl-dialog__title").html("Add password");
    $("#insert-password-dialog .delete-password-btn").hide();
    $("#insert-password-dialog button[type=submit]").html("Add");
  });

  // Edit an existing password
  $(".edit-password-btn")
      .click(
          function() {
            document.querySelector('#insert-password-dialog').showModal();
            var entityKey = $(this).find(".entity-key").html();
            var service = $(this).find(".service").html();
            var username = $(this).find(".username").html();
            var password = $(this).find(".password").html();
            $("#insert-password-dialog input[name=password_entity_key]").val(
                entityKey);

            // Note that I had to use change the mdl way to get the input label to float up.
            // See: https://github.com/google/material-design-lite/issues/1287
            document.querySelector('#service-field').MaterialTextfield
                .change(service);
            document.querySelector('#username-field').MaterialTextfield
                .change(username);
            document.querySelector('#password-field').MaterialTextfield
                .change(password);
            $("#insert-password-dialog .service-for-delete").html(service);
            $("#insert-password-dialog .entity-key-for-delete").html(entityKey);
            $("#insert-password-dialog .mdl-dialog__title").html(
                "Update password");
            $("#insert-password-dialog .delete-password-btn").show();
            $("#insert-password-dialog button[type=submit]").html("Update");
          });

  // Password cancel button to close the insert-password-dialog
  $('.close-insert-password-dialog').click(function() {
    document.querySelector('#insert-password-dialog').close();
  });

  // Clicked the button to show the delete password confirmation screen.
  $(".delete-password-btn").click(function() {
    document.querySelector('#insert-password-dialog').close();
    document.querySelector('#delete-password-dialog').showModal();
    var service = $(this).find(".service-for-delete").html();
    var entityKey = $(this).find(".entity-key-for-delete").html();
    $("#delete-password-service").html(service);
    $("input[name=password_to_delete_key]").val(entityKey);
  });

  // Cancel button on the delete confirmation dialog.
  $('.close-delete-password-dialog').click(function() {
    document.querySelector('#delete-password-dialog').close();
  });
};


$(document).ready(function() {
  rh.pk.mdlInitializations();
  rh.pk.enableButtons();
});
