alert("its working")
$("ul").on("click","li",function () {
    $("li").removeClass("active")
    $(this).addClass("active")
})