$( document ).ready(function() {

    $('#file').change(function(){
         if  ($('#file').val()!='') {
             $('#file-label').text('');
             $('#file-label').addClass('done');
         }
     });

    $('.employee-show-more').click(function (){
        let id = $(this).attr('id');
        let showId = 'iframe-id-' + id.substr(13);
        $('#' + showId).toggleClass('hidden');
    });
});
