% rebase("base.tpl", title="Pregledovalec portfeljev")

<h1>Pregledovalec portfeljev</h1>
<div class="card bg-secondary mb-3">
  <div class="card-body">
    <p class="fs-5 fw-bold">
      Pozdravljen/-a {{ime}} in dobrodošel/-a v Pregledovalcu portfeljev!
    </p>
    <p>
      Pred tabo je program, ki ti s pomočjo
      <a class="link text-dark" href="https://www.coinlore.com/cryptocurrency-data-api">API</a>-ja
      omogoča spremljanje aktualnih cen kriptovalut in njihovih kombinacij, ki jih lahko združiš
      v svoje portfelje.
    </p>
    % if uporabnisko_ime:
    <p>
      S pomočjo spodnjih gumbov lahko pogledaš svoje portfelje in njihove donose, ustvariš nov
      portfelj, pogledaš podatke o različnih kriptovalutah ali pa se odjaviš in prijaviš z
      drugim računom.
    </p>
    <div class="col px-2">
      <div class="row mb-2" width="100%">
        <div class="col d-grid px-1">
          <a class="btn btn-dark btn-block" href="/moji-portfelji/">Moji portfelji</a>
        </div>
        <div class="col d-grid px-1">
          <a class="btn btn-dark btn-block" href="/kriptovalute/90/">Pregled kriptovalut</a>
        </div>
      </div>
      <div class="row" width="100%">
        <div class="col d-grid px-1">
          <a class="btn btn-dark btn-block" href="/nov-portfelj/">Ustvari nov portfelj</a>
        </div>
        <div class="col d-grid px-1">
          <a class="btn btn-dark btn-block" href="/odjava/">Odjava</a>
        </div>
      </div>
    </div>

    % else:
    <p>
      Za dostop do vseh funkcij moraš biti prijavljen.
      Če že imaš uporabniški račun, se s klikom na spodnji gumb prijavi. Če računa še nimaš, ga
      lahko enostavno ustvariš s klikom na gumb <i> Registracija</i>.
    </p>
    <div class="row" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/prijava/">Prijava</a>
      </div>
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/registracija/">Registracija</a>
      </div>
    </div>
    % end
  </div>
</div>

% if not uporabnisko_ime:
<div class="card bg-dark border-secondary mb-3">
  <div class="card-body text-secondary py-1">
    <p class="mb-0">Uporabniški račun za demonstracijo je na voljo z uporabniškim imenom 
      <i>Demo</i> in geslom
      <i>geslo</i>.
    </p>
  </div>
</div>
% end
