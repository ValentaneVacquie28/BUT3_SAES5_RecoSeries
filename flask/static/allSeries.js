$(document).ready(function () {
    console.log("Page All Séries chargée avec succès.");

    // Fonction pour envoyer un feedback (like/dislike)
    function sendFeedback(serieId, action, button) {
        if (!serieId || serieId.trim() === "") {  // Vérification des IDs vides ou non valides
            console.error("ID de série invalide :", serieId);
            alert("ID de série invalide.");
            return;
        }

        $.ajax({
            url: '/feedback',
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({ id: serieId, action: action }),
            success: function (response) {
                if (response.success) {
                    const parent = $(button).closest(".buttons");
                    parent.find(".like-btn").removeClass("active").css("background-color", "");
                    parent.find(".dislike-btn").removeClass("active").css("background-color", "");

                    if (action === "like") {
                        $(button).addClass("active").css("background-color", "green");
                    } else if (action === "dislike") {
                        $(button).addClass("active").css("background-color", "red");
                    }
                } else {
                    alert(response.message || "Erreur lors de l'envoi des données.");
                }
            },
            error: function () {
                alert("Une erreur est survenue, veuillez réessayer.");
            },
        });
    }

    // Fonction pour charger les séries en fonction de la page
    function loadSeries(page) {
        $.get('/all_series', { page: page }, function (data) {
            // Mettre à jour la liste des séries
            const seriesHtml = $(data).find("#seriesList").html();
            $("#seriesList").html(seriesHtml);

            // Mettre à jour les boutons de pagination
            const paginationHtml = $(data).find("#pagination").html();
            $("#pagination").html(paginationHtml);
        });
    }

    // Gérer les clics sur les boutons de pagination
    $(document).on('click', '.pagination-btn', function () {
        const page = $(this).data('page');
        loadSeries(page);
    });

    // Gestion des clics sur les boutons "Like"
    $(document).on('click', '.like-btn', function () {
        const button = $(this);
        const serieId = button.data('id');
        console.log("ID Série récupéré :", serieId);
        sendFeedback(serieId, "like", button);
    });

    // Gestion des clics sur les boutons "Dislike"
    $(document).on('click', '.dislike-btn', function () {
        const button = $(this);
        const serieId = button.data('id');
        console.log("ID Série récupéré :", serieId);
        sendFeedback(serieId, "dislike", button);
    });

    // Charger la page initiale des séries
    const currentPage = {{ page }};  // Vous pouvez obtenir la page actuelle de Flask
    loadSeries(currentPage);
});