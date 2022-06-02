
const regularlyCheckbox = () => {
    $(".regularly_order_checkbox").on('click', function() {
        let route_name = $(this).parent().next().next().text();
        let number = $(this).parent().next().text();
        let value = $(this).val();
        if ($(this).prop('checked')) {
            
            var tr = $('<tr class="list_table_cell__tbody__tr"><td class="dispatch_regularly_order_group_td_check"></td><td class="dispatch_regularly_order_group_td_num"></td></tr>');
            
            var td_route = $(`<td class="dispatch_regularly_order_group_td_routename group_in_route${number}">${route_name}</td>`);
            
            $(".group_order__tbody").append(tr);
            $(".group_order__tbody .list_table_cell__tbody__tr:last-child").append(td_route);
            //노선 값 히든인풋
            $(".group_order__tbody .list_table_cell__tbody__tr:last-child").append($(`<input type="hidden" name="route" value="${value}">`))

        } else {
            "aaa", $(`input[type=hidden][value=${value}]`).parent().remove();

        }
        
    })
};

const deleteButton = () => {
    if (confirm("정말로 삭제하시겠습니까?")){
        const form = document.getElementById("deleteFormCreateForm");
        const groupId = document.getElementById('groupid').value;
        const url = `http://kingbuserp.link/dispatch/regularly/group/${groupId}/delete/`
        form.action = url;
    }
    


}

regularlyCheckbox();