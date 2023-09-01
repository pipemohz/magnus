$(document).ready(function () {
    var counter = 0;
    var records;
    var batchRecords;
    var paginationSize;
    var pageActive;
    const ulFilter = document.getElementById("filter-list");
    const ulResults = document.getElementById("results-cards");
    const ulPagination = document.getElementById("pagination");
    const text = document.getElementById("search-text");
    const quantity = document.getElementById("quantity");
    const modal = document.getElementById("modal");
    const closeModal = document.getElementById("close-modal");
    const Url = "/ai/api/search/";
    var one_star
    var two_stars
    
    $("#search-text").keyup(function(event) {
        if (event.which === 13) {
            $("#search-btn").click();
        }
    });

    $('#search-btn').click(function () {
        var keywords = [];

        if (ulFilter.hasChildNodes()) {
            for (item of ulFilter.children) {
                keywords.push(item.firstChild.value)
            }

        }

        const data = {
            text: text.value,
            keywords: keywords,
            quantity: quantity.value
        }

        $("#results-title").text("");
        $("#results-status").text("");
        $("#loader-spinner").removeAttr("hidden");

        if (ulResults.hasChildNodes()) {
            $("#results-cards").empty();
        }

        if (ulPagination.hasChildNodes()) {
            $("#pagination").empty();
        }

        $.ajax({
            url: Url,
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json",
            type: "POST",
            success: function (data) {
                $("#results-title").text("Resultados");
                $("#results-status").text("Busqueda Completada");
                records = data['records']
                console.log(records)

                // records = JSON.parse(data['records']);
                // console.log(records)

                $("#loader-spinner").attr("hidden", "");
                if (records.length === 0) {
                    $("#results-status").text("No se han encontrado canditados adecuados");
                    return
                }
                // Define the limits of the califications for the registers
                var array_similarity = records.map(record => record.similarity);
                var max_similarity = array_similarity[0]
                var min_similarity = 0.83//array_similarity[array_similarity.length - 1]
                var range_similarity = max_similarity-min_similarity

                one_star = 0.85//range_similarity * 0.4 + min_similarity
                two_stars = 0.863//range_similarity * 0.7 + min_similarity


                paginationSize = 10
                const numberPages = Math.ceil(records.length/paginationSize);
                
                batchRecords = records.slice(0, paginationSize);
                
                for (var i = 1; i <= numberPages; i += 1) {
                    idPage = `page-${i}`;
                    page = `<li><a id="${idPage}" aria-label="${i}">${i}</a></li>`;
                    pageActive = idPage;
                    $("#pagination").append(page);
                    document.getElementById(idPage).addEventListener("click", renderPagination);

                }
                
                document.getElementById("page-1").click();
                
            },
            error: function (error) {
                console.log(`Error ${error}`)
                $("#results-status").text("An error has ocurred during search_text process");
                $("#loader-spinner").attr("hidden", "");
            }
        })
        
    });

    function openModal(event){
        index = Number(event.currentTarget.getAttribute("aria-label"));
        record = batchRecords[index];
        modal.children[0].children[1].children[0].textContent = record.abstract;
        modal.children[0].children[2].children[0].href = record.web_url;
        modal.showModal();
    }

    closeModal.addEventListener("click", () =>{
        modal.close();
    });

    function renderPagination(event){
        index = Number(event.currentTarget.getAttribute("aria-label"))

        if (ulResults.hasChildNodes()) {
            $("#results-cards").empty();
        }
        start = (index-1)*paginationSize
        end = (index*paginationSize)
        batchRecords = records.slice(start, end);
        renderCards(batchRecords);
        idPage = event.currentTarget.getAttribute("id")
        $(`#${pageActive}`).removeAttr("class")
        $(`#${idPage}`).attr("class", "active");
        pageActive = idPage
    }

    function renderCards(batchRecords){
        var card = "";
        var match = "";
        var updateData = "";
        for (var i = 0; i < batchRecords.length; i += 1) {

            if (batchRecords[i]['similarity'] >= two_stars) {
                match = "\u2658\u2658\u2658";
            } else if (batchRecords[i]['similarity'] > one_star && batchRecords[i]['similarity'] < two_stars) {
                match = "\u2658\u2658";
            } else {
                match = "\u2658";
            }

            updateData = batchRecords[i]['updated_at'].split("T")[0]
            idCard = `card-${i}`
            card = `<div id="${idCard}" class="card" aria-label="${i}" ><div><h3>${match}</h3></div><div><h4>${batchRecords[i]['filename']}</h4></div><div><p>Última modificación: ${updateData}</p></div></div>`
            // `<a href="${records[i]['web_url']}" target="_blank"><figure><div class="card"><div><h3>${match}</h3></div><div><h4>${records[i]['filename']}</h4></div><div><p>Última modificación: ${updateData}</p></div></div><div class="abstract"><p>${records[i]['abstract']}</p></div></figure></a>`;

            $("#results-cards").append(card);
            document.getElementById(idCard).addEventListener("click", openModal);
        }
    }

    $("#add-filter").click(function () {
        if (counter < 5){
            $("#filter-list").append('<li><input type="text" class="form-control" aria-describedby="searchHelp"></li>');
            counter += 1;
        }
        else {
            alert("Sólo se pueden agregar máximo 5 filtros.");
        }
    });

    $("#remove-filter").click(function () {
        if (ulFilter.hasChildNodes()) {
            ulFilter.removeChild(ulFilter.lastChild);
        }
        if (counter > 0) {
            counter -= 1;
        }

    });

});