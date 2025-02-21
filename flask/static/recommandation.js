$(document).ready(function () {
    console.log("Page Recommandations chargée avec succès.");

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

    // Récupérer les séries likées et dislikées au démarrage de la page
    function updateButtons() {
        $.get('/getLikes', function (likedSeries) {
            likedSeries.forEach(function (serieId) {
                const button = $(`.like-btn[data-id="${serieId}"]`);
                button.addClass("active").css("background-color", "green");
            });
        });
        $.get('/getDislikes', function (dislikedSeries) {
            dislikedSeries.forEach(function (serieId) {
                const button = $(`.dislike-btn[data-id="${serieId}"]`);
                button.addClass("active").css("background-color", "red");
            });
        });
    }

    updateButtons();  // Mettre à jour les boutons dès que la page est chargée

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
});