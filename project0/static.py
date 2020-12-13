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
        <h4 style="margin-top: 1rem;">Обновить лекарство</h4>
        <label for="drugSelect">Лекарство</label>
        <select class="form-control" id="drugSelect"></select>
        <label for="pharmacySelect">Аптека</label>
        <select class="form-control" id="pharmacySelect"></select>
        <label for="quantityInput">Количество</label>
        <input type="number" class="form-control" id="quantityInput"/>
        <label for="priceInput">Цена</label>
        <input type="number" class="form-control" id="priceInput"/>
        <button
            style="margin-top: 2rem;"
            class="form-control"
            id="updateGoodButton">
        Обновить
        </button>

        <h4 style="margin-top: 1rem;"> Перераспределить лекарство </h4>
        <label for="drugSelect2">Лекарство</label>
        <select class="form-control" id="drugSelect2"></select>
        <label for="remainderInput">Минимально допустимый остаток</label>
        <input type="number" class="form-control" id="remainderInput"/>
        <label for="profitInput">Целевое увеличение прибыли</label>
        <input type="number" class="form-control" id="profitInput"/>
        <button
            style="margin-top: 2rem;"
            class="form-control"
            id="redistributeButton">
        Перераспределить
        </button>
    </div>
</form>
<script lang="js">
    function loadData() {
        const drugSelect = $('#drugSelect');
        const drugSelect2 = $('#drugSelect2');
        $.getJSON('/drugs', function (drugs) {
           drugs.forEach(function (value) {
               value = JSON.parse(value);
               $("<option>").text(value.trade_name).attr("value", value.id)
                   .appendTo(drugSelect);
               $("<option>").text(value.trade_name).attr("value", value.id)
                   .appendTo(drugSelect2);
           })
        });
        const pharmacySelect = $('#pharmacySelect');
        $.getJSON('/pharmacies', function (pharmacies) {
            pharmacies.forEach(function (value) {
                value = JSON.parse(value);
                $("<option>").text(value.name).attr("value", value.id)
                    .appendTo(pharmacySelect);
            });
        });
        $('#updateGoodButton').click(function() {
            const drugSelect = $('#drugSelect');
            const pharmacySelect = $('#pharmacySelect');
            const quantityInput = $('#quantityInput');
            const priceInput = $('#priceInput');
            $.post("/update_retail", {
                "drug_id": drugSelect.val(),
                "pharmacy_id": pharmacySelect.val(),
                "remainder": quantityInput.val(),
                "price": priceInput.val(),
            });
        });
        $('#redistributeButton').click(function() {
            const drugSelect = $('#drugSelect2');
            const profitInput = $('#profitInput');
            const remainderInput = $('#remainderInput');
            $.post("/drug_move", {
                "drug_id": drugSelect.val(),
                "target_income_increase": profitInput.val(),
                "min_remainder": remainderInput.val(),
            }).done(function(response) {
                console.log(response);
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
