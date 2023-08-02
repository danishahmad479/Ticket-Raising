$(document).ready(function(){         
    $(window).on("beforeunload", function(e) {
        $.ajax({
                url: logout,
                method: 'GET',
            })
    });
})

