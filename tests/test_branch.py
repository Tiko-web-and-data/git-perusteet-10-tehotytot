import sys
import subprocess
    
def get_branches():
    try:
        result = subprocess.run(  # Haetaan branchit remotesta, koska Github ei löydä brancheja paikallisella komennolla
            ['git', 'branch', '-r'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)   
    
    rawBranches = result.stdout.split("\n")
    branches = []

    rawBranches.pop() # Poistetaan tyhjä solu listasta
    for branch in rawBranches : # Lisätään toiseen listaan ainoastaan tarpeellisten haarojen nimet
        if branch != "  origin/HEAD -> origin/main" and branch != "  origin/develop" and branch != "  origin/main" :
            branches.append(branch) 

    return branches

def check_recipe_content(): # Otetaan talteen HTML-tiedosto ja muutetaan kirjainkoko pieneksi
    html = open("recipe.html", 'r')
    file_content = html.read()
    encoded_file = file_content.encode()
    return encoded_file.lower()

def compareNames(branchNames, recipe_content): # Verrataan löytyykö branchien opiskelijatunnukset html-tiedostosta
    matches = []

    for name in branchNames :
        iterable = name.lower().strip().encode()
        if recipe_content.count(iterable[7:]) : # poistetaan 7 ensimmäistä merkkiä, jotta "origin/" jää vertailusta pois
            matches.append(iterable)
    
    return matches  
         
def main():
    branchNames = get_branches() # Haetaan branchit
    recipe_content = check_recipe_content() # Haetaan HTML
    matches = compareNames(branchNames, recipe_content) # Tarkistetaan yhtäläisyydet
    
    for branch in matches :
        print(f"Haaralle {branch[7:].decode()} löytyi vastaava resepti recipe.html -tiedostosta")

    print(f"{len(matches)} opiskelijaa on lisännyt pitsatäytteet omalta haaraltaan")
    if len(matches) > 2 :
        print("Reseptejä on lisätty tarpeeksi")
    else: 
        print("Lisätkää reseptit omilta haaroiltanne ja käyttäkää opiskelijatunnusta haaran nimenä sekä pitsareseptin otsikossa")
        sys.exit(1)

if __name__ == "__main__":
    main()
