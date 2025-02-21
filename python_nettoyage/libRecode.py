import regex as re

def recode(contenu):
    # Remplace les Ã© par des é
    contenu = contenu.replace('Ã©', 'é')
    # Remplace les Ã¨ par des è
    contenu = contenu.replace('Ã¨', 'è')
    # Remplace les Ãª par des ê
    contenu = contenu.replace('Ãª', 'ê')
    # Remplace les Ã´ par des ô
    contenu = contenu.replace('Ã´', 'ô')
    # Remplace les Ã® par des î
    contenu = contenu.replace('Ã®', 'î')
    # Remplace les Ã§ par des ç
    contenu = contenu.replace('Ã§', 'ç')
    # Remplace les Ã« par des ë
    contenu = contenu.replace('Ã«', 'ë')
    # Remplace les Ã¢ par des â
    contenu = contenu.replace('Ã¢', 'â')
    # Remplace les Ã par des à
    contenu = contenu.replace('Ã', 'à')
    # Remplace les à» par des û
    contenu = contenu.replace('à»', 'û')
    # Remplace à¼ par û
    contenu = contenu.replace('à¼', 'û')
    # Remplace Â° par °
    contenu = contenu.replace('Â°', '°')
    # Remplace à§ par ç
    contenu = contenu.replace('à§', 'ç')
    # Remplace àª par ê
    contenu = contenu.replace('àª', 'ê')
    # Remplace à¨ par è
    contenu = contenu.replace('à¨', 'è')
    # Remplace à® par î
    contenu = contenu.replace('à®', 'î')
    # Remplace à´ par ô
    contenu = contenu.replace('à´', 'ô')
    # Remplace à¢ par â
    contenu = contenu.replace('à¢', 'â')
    # Remplace à« par ë
    contenu = contenu.replace('à«', 'ë')
    # Remplace à¹ par ù
    contenu = contenu.replace('à¹', 'ù')
    # Remplace àˆ par Ê
    contenu = contenu.replace('àˆ', 'Ê')
    # Remplace à‰ par É
    contenu = contenu.replace('à‰', 'É')
    # Remplace àŠ par È
    contenu = contenu.replace('àŠ', 'È')
    # Remplace à‡ par Ç
    contenu = contenu.replace('à‡', 'Ç')
    # Remplace à˜ par Ô
    contenu = contenu.replace('à˜', 'Ô')
    # Remplace àŽ par Û
    contenu = contenu.replace('àŽ', 'Û')
    # Remplace à™ par Û
    contenu = contenu.replace('à™', 'Û')
    # Remplace àŒ par Û
    contenu = contenu.replace('àŒ', 'Û')
    # Remplace à€ par À
    contenu = contenu.replace('à€', 'À')
    # Remplace àŸ par Ù
    contenu = contenu.replace('àŸ', 'Ù')
    # Remplace à¸ par ù
    contenu = contenu.replace('à¸', 'ù')
    # Remplace à¥ par ÿ
    contenu = contenu.replace('à¥', 'ÿ')
    # Remplace à‹ par Ë
    contenu = contenu.replace('à‹', 'Ë')
    # Remplace à” par Ô
    contenu = contenu.replace('à”', 'Ô')
    # Remplace à‹ par Ë
    contenu = contenu.replace('à‹', 'Ë')
    print("Recode terminé")
    return contenu