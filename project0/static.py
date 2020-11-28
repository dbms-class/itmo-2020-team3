def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Фуфломицины</title>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
</head>
<body>
<form class="col-6">
    <div class="form-group">
        <label for="drugSelect">Лекарство</label>
        <select class="form-control" id="drugSelect"></select>
        <label for="pharmacySelect">Аптека</label>
        <select class="form-control" id="pharmacySelect"></select>
        
        <h4 style="margin-top: 3rem;">Обновление лекарства</h4>
        <label for="drugInput">Аптека</label>
        <input class="form-control" id="drugInput"/>
        <label for="pharmacyInput">Лекарство</label>
        <input class="form-control" id="pharmacyInput"/>
        <label for="quantityInput">Количество</label>
        <input type="number" class="form-control" id="quantityInput"/>
        <label for="priceInput">Цена</label>
        <input type="number" class="form-conctrol" id="priceInput"/>
        <button
            style="margin-top: 2rem;"
            class="form-control"
            id="updateGoodButton">
        Обновить
        </button>
    </div>
</form>
<script lang="js">
    function loadData() {
        const drugSelect = $('#drugSelect');
        $.getJSON('/drugs', function (drugs) {
           drugs.forEach(function (value) {
               $("<option>").text(value.name).attr("value", value.id)
                   .appendTo(drugSelect);
           })
        });
        const pharmacySelect = $('#pharmacySelect');
        console.log(pharmacySelect);
        $.getJSON('/pharmacies', function (pharmacies) {
            console.log(pharmacySelect);
            pharmacies.forEach(function (value) {
                $("<option>").text(value.name).attr("value", value.id)
                    .appendTo(pharmacySelect);
            });
        });
        $('#updateGoodButton').click(function() {
            const drugInput = $('#drugInput');
            const pharmacyInput = $('#pharmacyInput');
            const quantityInput = $('#quantityInput');
            const priceInput = $('#priceInput');
            $.post("/update_retail", {
                "drug_id": drugInput.val(),
                "pharmacy_id": pharmacyInput.val(),
                "remainder": quantityInput.val(),
                "price": priceInput.val(),
            });
        });
    }
    $(document).ready(function () {
        loadData();
    });
</script>
</body>
</html>
  """
