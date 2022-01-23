$(function(){

  $('#create_directory_bg').hide()
  $('#select_address_bg').hide()
  $('#setting_file_bg').hide()
  $('#complete_share_file_bg').hide()
  $('#file_size_over_alert_bg').hide()

  $('#create_directory_btn').click(function(){
    $('#create_directory_bg').fadeIn(300);
  })

  function set_directory_data(response){
    for(var key in response.directory_data){
      var directory_data = '<li class="stoppo_item"><a href="javascript:void(0);" name="'+response.directory_data[key].directory+'" class="change_directory"><img src="/static/image/guide_folder.png" style="margin-right:0.5vw;" class="file_image"><p class="file_name">'+response.directory_data[key].directory_name+'</p></a><div class="action_btn_container"><a href="javascript:void(0)" name="'+response.directory_data[key].directory+'" class="setting_file_btn"><img src="/static/image/guide_detail.png" class="guide_image file_image"></a></div></li>'
      $('#directory_box').append(directory_data).trigger('create')
    }
    $('#upward_directory_id').val(upward_directory_id)

    for(var key in response.current_directory_file){
      switch(response.current_directory_file[key].extension){
        case '.pdf':
          var directory_file = '<li class="stoppo_item"><a href="/stoppo/file_view/'+response.current_directory_file[key].upload_file_id+'" target="_blank" name="'+response.current_directory_file[key].upload_file_id+'" class="show_detail"><img src="/static/image/guide_pdf.png" style="margin-right:0.5vw;" class="file_image"><p class="file_name">'+response.current_directory_file[key].file_name+'</p></a><div class="action_btn_container"><a name="'+response.current_directory_file[key].upload_file_id+'" href="javascript:void(0);" class="file_share_btn"><img src="/static/image/guide_share.png" class="guide_image file_image"></a><a href="javascript:void(0);" name="'+response.current_directory_file[key].upload_file_id+'" class="setting_file_btn"><img src="/static/image/guide_detail.png" class="guide_image file_image"></a></div></li>'
          break;

        case '.jpg':
          var directory_file = '<li class="stoppo_item"><a href="/stoppo/file_view/'+response.current_directory_file[key].upload_file_id+'" target="_blank" name="'+response.current_directory_file[key].upload_file_id+'" class="show_detail"><img src="/static/image/guide_image.png" style="margin-right:0.5vw;" class="file_image"><p class="file_name">'+response.current_directory_file[key].file_name+'</p></a><div class="action_btn_container"><a name="'+response.current_directory_file[key].upload_file_id+'" href="javascript:void(0);" class="file_share_btn"><img src="/static/image/guide_share.png" class="guide_image file_image"></a><a href="javascript:void(0);" name="'+response.current_directory_file[key].upload_file_id+'" class="setting_file_btn"><img src="/static/image/guide_detail.png" class="guide_image file_image"></a></div></li>'
          break;

        case '.pptx':
          var directory_file = '<li class="stoppo_item"><a href="/stoppo/file_view/'+response.current_directory_file[key].upload_file_id+'" target="_blank" name="'+response.current_directory_file[key].upload_file_id+'" class="show_detail"><img src="/static/image/guide_pptx.png" style="margin-right:0.5vw;" class="file_image"><p class="file_name">'+response.current_directory_file[key].file_name+'</p></a><div class="action_btn_container"><a name="'+response.current_directory_file[key].upload_file_id+'" href="javascript:void(0);" class="file_share_btn"><img src="/static/image/guide_share.png" class="guide_image file_image"></a><a href="javascript:void(0);" name="'+response.current_directory_file[key].upload_file_id+'" class="setting_file_btn"><img src="/static/image/guide_detail.png" class="guide_image file_image"></a></div></li>'
          break;

        case '.xlsx':
          var directory_file = '<li class="stoppo_item"><a href="/stoppo/file_view/'+response.current_directory_file[key].upload_file_id+'" target="_blank" name="'+response.current_directory_file[key].upload_file_id+'" class="show_detail"><img src="/static/image/guide_xlsx.png" style="margin-right:0.5vw;" class="file_image"><p class="file_name">'+response.current_directory_file[key].file_name+'</p></a><div class="action_btn_container"><a name="'+response.current_directory_file[key].upload_file_id+'" href="javascript:void(0);" class="file_share_btn"><img src="/static/image/guide_share.png" class="guide_image file_image"></a><a href="javascript:void(0);" name="'+response.current_directory_file[key].upload_file_id+'" class="setting_file_btn"><img src="/static/image/guide_detail.png" class="guide_image file_image"></a></div></li>'
          break;


        default:
          var directory_file = '<li class="stoppo_item"><a href="/stoppo/file_view/'+response.current_directory_file[key].upload_file_id+'" target="_blank" name="'+response.current_directory_file[key].upload_file_id+'" class="show_detail"><img src="/static/image/guide_file.png" style="margin-right:0.5vw;" class="file_image"><p class="file_name">'+response.current_directory_file[key].file_name+'</p></a><div class="action_btn_container"><a name="'+response.current_directory_file[key].upload_file_id+'" href="javascript:void(0);" class="file_share_btn"><img src="/static/image/guide_share.png" class="guide_image file_image"></a><a href="javascript:void(0);" name="'+response.current_directory_file[key].upload_file_id+'" class="setting_file_btn"><img src="/static/image/guide_detail.png" class="guide_image file_image"></a></div></li>'
          break;
      }
      $('#directory_box').append(directory_file).trigger('create')
    }
  }


  const target = document.getElementById('directory_box');

  const observer = new MutationObserver(function () {
    var url = new URL(window.location.href);
    var params = url.pathname.split('/');
    var upward_directory_id = params.slice(-2)[0]


    $('#upward_directory_id').val(upward_directory_id)
  })

  const config = {
    childList: true,
    characterData: true,
    characterData: true,
    subtree: true
  };

  observer.observe(target, config);

  function reload(){
    $.ajax({
      type:'GET',
      url:'/stoppo/get_directory_data/',
      data:{
        "upward_directory_id":$('#upward_directory_id').val(),
      },
      success:function(response){
        $('.stoppo_item').remove()
        set_directory_data(response)
      },
      error:function(response){
      }
    })
  }

  $(document).on('click','.setting_file_btn',function(){
    var file_id = $(this).attr('name')
    $('#selecting_file_id').val(file_id)
    $('#setting_file_bg').fadeIn(300);
    $.ajax({
      type:'GET',
      url:'/stoppo/get_file_name/'+file_id+'/',
      success:function(response){
        $('#change_file_name').val(response.file_name)
      },
      error:function(response){
      }
    })
  })

  $('#back_btn').click(function(){
    window.history.back(-1);
    window.setTimeout(back_directory,100)
    function back_directory(){
      var url = new URL(window.location.href);
      var params = url.pathname.split('/');
      var upward_directory_id = params.slice(-2)[0]
      $('.stoppo_item').remove()
      $.ajax({
        type:'GET',
        url:'/stoppo/get_directory_data/',
        data:{
          'upward_directory_id' : upward_directory_id,
        },
        success:function(response){
          set_directory_data(response)
        },
        error:function(response){
        },
      })
    }


  })

  $('#submit_create_directory_btn').click(function(){
    var url = new URL(window.location.href);
    var params = url.pathname.split('/');

    var new_directory_name = $('#new_directory_name').val()
    $.ajax({
      type:'GET',
      url:'/stoppo/create_directory/',
      data:{
        'new_directory_name':new_directory_name,
        'upward_directory_id':params.slice(-2)[0],
      },
      success:function(response){
        $('#create_directory_bg').fadeOut(300);
        reload()
      },
      error:function(response){
      }
    })
  })

  $(document).on('click','.change_directory',function(){
    var upward_directory_id = $(this).attr('name')
    var current_url = new URL(window.location.href);
    history.pushState(null,null,current_url.href+upward_directory_id+'/')
    $('.stoppo_item').remove()
    $.ajax({
      type:'GET',
      url:'/stoppo/get_directory_data/',
      data:{
        'upward_directory_id' : upward_directory_id,
      },
      success:function(response){
        set_directory_data(response)
        $('#upward_directory_id').val(upward_directory_id)
      },
      error:function(response){
      },
    })
  })

  $(document).on('click','.file_share_btn',function(){
    var file_name = $(this).html()
    $('#share_file_id').val($(this).attr('name'))
    $('#select_address_bg').fadeIn(300);
  })

  $(document).on('click','.address_card_link',function(){
    var address = $(this).attr('name')
    var share_directory_id = $('#share_file_id').val()
    $.ajax({
      type:'GET',
      url:'/stoppo/share_file/',
      data:{
        'address':address,
        'share_directory_id':share_directory_id,
      },
      success:function(response){
        $('#complete_share_file_bg').fadeIn(100);
        setTimeout(() => {
            $('#complete_share_file_bg').fadeOut(350);
        }, 500);
      },
      error:function(response){
      }
    })
  })

  $('.address_card_link').click(function(){
    $('#select_address_bg').hide()
  })

  $('#change_file_name_btn').click(function(){
    var file_id = $('#selecting_file_id').val()
    var new_file_name = $('#change_file_name').val()
    if(new_file_name.length > 1){
      $.ajax({
        type:'GET',
        url:'/stoppo/change_file_name/'+file_id+'/',
        data:{
          'new_file_name':new_file_name
        },
        success:function(response){
          $('#setting_file_bg').fadeOut(300)
          reload()
        },
        error:function(response){
        }
      })
    }
  })

  $('#detaile_link').click(function(){
    var file_id = $('#selecting_file_id').val()
    $.ajax({
      type:'GET',
      url:'/stoppo/delete_file/'+file_id+'/',
      success:function(response){
        $('#setting_file_bg').fadeOut(300)
        reload()
      },
      error:function(response){
      }
    })
  })

  $(document).on('click',function(e) {
     if(!$(e.target).closest('#create_directory_form').length && $(e.target).closest('#create_directory_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#create_directory_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });

  $(document).on('click',function(e) {
     if(!$(e.target).closest('#setting_file').length && $(e.target).closest('#setting_file_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#setting_file_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });

  $(document).on('click',function(e) {
     if(!$(e.target).closest('#select_address').length && $(e.target).closest('#select_address_bg').length) {
       // ターゲット要素の外側をクリックした時の操作
       $('#select_address_bg').fadeOut(300)
     } else {
       // ターゲット要素をクリックした時の操作
     }
  });

})
