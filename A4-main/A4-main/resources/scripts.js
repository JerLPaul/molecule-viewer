
$(window).on('load',
    function () {
        getElementList();

        currForm = $('#formFrame').contents().find('#addElement');
        $('#formFrame').contents().find('#btn1').click(
            function() {

              currForm.hide();
              $('#formFrame').contents().find('#upload').show();
              $('#formFrame').contents().find('#errMsg').html(" ");
              currForm = $('#formFrame').contents().find('#upload');
            }
        );

        $('#formFrame').contents().find('#btn2').click(
            function() {
              $.post('/displayList',
                function(data, response) {
                  getMolList(data, response)
                }
              );
              currForm.hide();
              $('#formFrame').contents().find('#select').show();
              $('#formFrame').contents().find('#errMsg').html(" ");
              currForm = $('#formFrame').contents().find('#select');
            }
        );

        $('#formFrame').contents().find('#btn3').click(
            function() {
              getElementList();
              currForm.hide();
              $('#formFrame').contents().find('#addElement').show();
              $('#formFrame').contents().find('#errMsg').html(" ");
              currForm = $('#formFrame').contents().find('#addElement');
            }
        );

        $('#formFrame').contents().find('#btn4').click(
          function() {
            currForm.hide();
            $('#formFrame').contents().find('#rotate').show();
            $('#formFrame').contents().find('#errMsg').html(" ");
            currForm = $('#formFrame').contents().find('#rotate');


          }
      );

        $('#formFrame').contents().find('#uploadForm').submit(
            function(e) {
              e.preventDefault();

              if ($('#formFrame',  window.parent.document).contents().find('#molName').val() == "") {
                $('#formFrame', window.parent.document).contents().find('#errMsg').html("Please name the molecule");
                return;
              }
              var formData = new FormData($(this)[0]);

              $.ajax({
                url: '/molecule',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(data, response) {
                    list = data.split('\n');
                    newList = list.slice(3);
                    output = newList.join('\n');
                    $('#displayFrame', window.parent.document).contents().find('#displayMol').html(output);
                    $('#formFrame', window.parent.document).contents().find('#errMsg').html("Uploaded");
                  },
                error: function(err) {
                    $('#formFrame', window.parent.document).contents().find('#errMsg').html(err.responseText);
                  }
              });
            });

        $('#formFrame').contents().find('#elementForm').submit(
            function(e) {
              //POST THE FORM AND LET PARENT RECEIVE
              e.preventDefault();
              if ($('#formFrame').contents().find('#radius').val() <= 0) {
                $('#formFrame').contents().find('#errMsg').html("Enter a proper radius");
                return;
              }

              if ($('#formFrame').contents().find('#colour1').val() == "") {
                c1 = $('#formFrame').contents().find('#colour1').attr('value');
              }
              else {
                c1 = $('#formFrame').contents().find('#colour1').val();
              }
              if ($('#formFrame').contents().find('#colour2').val() == "") {
                c2 = $('#formFrame').contents().find('#colour2').attr('value');
              }
              else {
                c2 = $('#formFrame').contents().find('#colour2').val();
              }
              if ($('#formFrame').contents().find('#colour3').val() == "") {
                c3 = $('#formFrame').contents().find('#colour3').attr('value');
              }
              else {
                c3 = $('#formFrame').contents().find('#colour3').val();
              }

              $.post('/element',
              {
                  number: $('#formFrame').contents().find('#number').val(),
                  code: $('#formFrame').contents().find('#code').val(),
                  name: $('#formFrame').contents().find('#name').val(),
                  colour1: c1,
                  colour2: c2,
                  colour3: c3,
                  radius: $('#formFrame').contents().find('#radius').val()
              })

              .done(function(data) {
                $('#formFrame', window.parent.document).contents().find('#errMsg').html("Success");
                getElementList();
              })
              .fail(function(err) {
                $('#formFrame', window.parent.document).contents().find('#errMsg').html(err.responseText);
              });

            }
        );

        $('#formFrame').contents().find('#rotateForm').submit(
          function(e) {
            //POST THE FORM AND LET PARENT RECEIVE
            e.preventDefault();
            $.post('/rotation',
            {
                name: $('#formFrame').contents().find('#currMol').val(),
                xrot: $('#formFrame').contents().find('#xrot').val(),
                yrot: $('#formFrame').contents().find('#yrot').val(),
                zrot: $('#formFrame').contents().find('#zrot').val()
            })
              .done(function(data) {
                $('#displayFrame').contents().find('#displayMol').html(data);
              })
              .fail(function(err) {
                $('#formFrame', window.parent.document).contents().find('#errMsg').html(err.responseText);
              });
          }
      );
    }
);

function displayMol(e) {
    $.post('/displayMol', e.attr('id'),
        function(data, response) {
            if (response) {
              $('#displayFrame', window.parent.document).contents().find('#displayMol').html(data);
              $('#formFrame', window.parent.document).contents().find('#currMol').attr('value', e.attr('id'));
            }
        }
    );
}

function rmElement(e) {
  $.post('/rmElement', e.attr('id'))
  .done(function(data) {
    $('#formFrame', window.parent.document).contents().find('#errMsg').html(data);
    getElementList();
  })
  .fail(function(err) {
    $('#formFrame', window.parent.document).contents().find('#errMsg').html(err.responseText);
  });
}

function getMolList(data, response) {
  $('#formFrame', window.parent.document).contents().find('#displayList').html(data);
}

function getElementList() {
  $.post('/displayElements',
    function(data, response) {
      $('#formFrame', window.parent.document).contents().find('#elementTable').html(data);
    }
  );
}
