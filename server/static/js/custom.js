<!-- Popover Script -->
// $(function(){
//     (document).ready(function(){
//       ('[data-toggle="popover"]').popover();
//     });
// })
//
// /* This function updates the live content fields. */
// $(function(){
//     window.setInterval(function(){
//     loadNewArtNetData()
//     }, 100)
//
// function loadNewArtNetData(){
//     $.ajax({
//         url:"/_artnet_monitor",
//         type: "POST",
//         dataType: "json",
//         success: function(data){
//             $(artnet_data).replaceWith(data)
//         }
//     })
// }
// });