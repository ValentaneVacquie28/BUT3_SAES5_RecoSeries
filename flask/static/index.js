$(document).ready(function() {
    // Fonction pour envoyer un feedback (like/dislike)
    function sendFeedback(serieId, action, button) {
        if (!serieId || serieId === "undefined") {
            alert("Erreur : l'identifiant de la série est invalide.");
            return;
        }

        console.log("Données envoyées :", { id: serieId, action: action }); // Debugging

        $.ajax({
            url: `/feedback`,
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
        $.get('/getLikes', function(likedSeries) {
            likedSeries.forEach(function(serieId) {
                const button = $(`.like-btn[data-id="${serieId}"]`);
                button.addClass("active").css("background-color", "green");
            });
        });
        $.get('/getDislikes', function(dislikedSeries) {
            dislikedSeries.forEach(function(serieId) {
                const button = $(`.dislike-btn[data-id="${serieId}"]`);
                button.addClass("active").css("background-color", "red");
            });
        });
    }

    // Fonction qui exécute la recherche
    function searchSeries() {
        const input = $('#motSerie').val(); 
        const mots = input.trim().split(/\s+/);

        if (mots.length < 3 || mots.length > 10) {
            alert('Vous devez insérer 3 à 10 mots');
        } else {
            $.ajax({
                url: '/search',
                method: 'GET',
                data: { motSerie: input },
                success: function(response) {
                    $('#resultList').empty(); 
                    if (response.error) {
                        $('#resultList').append('<li>' + response.error + '</li>');
                    } else {
                        response.forEach(function(serie, index) {
                            const serieId = serie.Title || `Serie-${index}`; 
                            $('#resultList').append(`
                                <li class="resultItem">
                                    <div class="partGauche">
                                        <img src="${serie.Poster}" alt="Poster de ${serie.Title}">
                                    </div>
                                    <div class="partDroite">
                                        <strong>${serie.Title}</strong> - ${serie.Released}
                                        <div class="genreItem">
                                            <p>${serie.Genre}</p>
                                        </div>
                                        <p>Intrigue : ${serie.Plot}</p>
                                        <p>Acteurs : ${serie.Actors}</p>
                                        <p>Scénaristes : ${serie.Writer}</p>
                                        <p>Réalisateur : ${serie.Director}</p>
                                        <p>Récompenses : ${serie.Awards}</p>
                                        <div class="buttons">
                                            <button class="like-btn" data-id="${serieId}">
                                                <i class="fa fa-thumbs-up fa-lg" aria-hidden="true"></i>
                                            </button>
                                            <button class="dislike-btn" data-id="${serieId}">
                                                <i class="fa fa-thumbs-down fa-lg" aria-hidden="true"></i>
                                            </button>
                                        </div>
                                    </div>
                                </li>
                            `);
                        });

                        // Met à jour les boutons après la recherche
                        updateButtons();
                    }
                },
                error: function() {
                    alert('Une erreur est survenue lors de la recherche.');
                }
            });
        }
    }

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

    // Exécute la recherche lorsqu'on appuie sur "Entrée" dans le champ de recherche
    $('#motSerie').on('keypress', function(e) {
        if (e.which === 13) {
            e.preventDefault();
            searchSeries();
        }
    });

    // Exécute la recherche lorsqu'on clique sur le bouton "Rechercher"
    $('#searchBtn').on('click', function() {
        searchSeries();
    });
});
