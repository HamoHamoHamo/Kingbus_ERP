function printDiv(divId) {

    var printContents = document.getElementById(divId).innerHTML;

    var originalContents = document.body.innerHTML;


    document.body.innerHTML = "<head><title>Print</title></head><body>" + printContents + "</body>";

    window.print();

   
    document.body.innerHTML = originalContents;


    window.location.reload(); 
}
