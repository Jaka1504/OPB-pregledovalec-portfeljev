% rebase("base.tpl", title="Kriptovaluta " + kriptovaluta["ime"])

% skupna_kolicina = sum([transakcija["kolicina"] for transakcija in kriptovaluta["transakcije"]])
% skupna_cena = sum([transakcija["kolicina"] * transakcija["cena_enote"] for transakcija in kriptovaluta["transakcije"]])
% skupna_vrednost = skupna_kolicina * kriptovaluta["vrednost_enote"]
% skupen_donos = skupna_vrednost - skupna_cena

<h1>Kriptovaluta {{kriptovaluta["ime"]}} v portfelju {{kriptovaluta["ime_portfelja"]}}</h1>
<div class="card bg-secondary mb-6">
  <div class="card-header">
    <h3>Podrobnosti</h3>
  </div>
  <div class="card-body py-0">
    <div class="container">
      <div class="row">
        <div class="col">
          <table class="table text-light">
            <tbody>
              <tr><td class="py-0">Ime</td><td class="py-0">{{kriptovaluta["ime"]}}</td></tr>
              <tr><td class="py-0">Kratica</td><td class="py-0">{{kriptovaluta["kratica"]}}</td></tr>
              <tr><td class="py-0">Količina</td><td class="py-0">{{f"{skupna_kolicina:.6f}"}}</td></tr>
              <tr><td class="py-0">Vrednost ene enote</td><td class="py-0">{{f"{kriptovaluta["vrednost_enote"]:.2f}"}}</td></tr>
              <tr>
                <td class="py-0">Trend</td>
                <td class="py-0">
                  % if kriptovaluta["trend"] >= 0: 
                  <span class="besedilo-zeleno">{{f"{kriptovaluta["trend"]:.2f}"}} % ▲</span>
                  % else:
                  <span class="besedilo-rdece">{{f"{kriptovaluta["trend"]:.2f}"}} % ▼</span>
                  % end
                </td>
              </tr>
              <tr><td class="py-0">Skupen vložek</td><td class="py-0">{{f"{skupna_cena:.2f}"}}</td></tr>
              <tr><td class="py-0">Skupna vrednost</td><td class="py-0">{{f"{skupna_vrednost:.2f}"}}</td></tr>
              <tr><td class="py-0">Donos</td><td class="py-0">{{f"{skupen_donos:.2f}"}}</td></tr>
            </tbody>
          </table>
        </div>
        <div class="col">
          Graf TBA
        </div>
      </div>
    </div>
  </div>
</div>

<div class="container-fluid text-dark">   <!-- To je precej cigansko, probej popravit -->
  .
</div>

<div class="card bg-secondary">
  <div class="card-header">
    <!-- <p class="mb-0">Ime: {{kriptovaluta["ime"]}}</p>
    <p class="mb-0">Kratica: {{kriptovaluta["kratica"]}}</p>
    <p class="mb-0">Količina: {{f"{skupna_kolicina:.6f}"}}</p>
    <p class="mb-0">Vrednost ene enote: {{f"{kriptovaluta["vrednost_enote"]:.2f}"}}</p>
    <p class="mb-0">Trend:
    % if kriptovaluta["trend"] >= 0: 
    <span class="besedilo-zeleno">{{f"{kriptovaluta["trend"]:.2f}"}} % ▲</span>
    % else:
    <span class="besedilo-rdece">{{f"{kriptovaluta["trend"]:.2f}"}} % ▼</span>
    % end
    </p>
    <p class="mb-0">Skupen vložek: {{f"{skupna_cena:.2f}"}}</p>
    <p class="mb-0">Skupna vrednost: {{f"{skupna_vrednost:.2f}"}}</p>
    <p class="mb-0">Donos: {{f"{skupen_donos:.2f}"}}</p>
    <p class="mb-0">Seznam transakcij:</p> -->
    <h3>Seznam transakcij</h3>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll-mala d-grid">
      <table class="table text-light">
        <thead class="fixed-head bg-secondary">
          <tr>
            <th scope="col" class="fixed-head">Datum nakupa</th>
            <th scope="col" class="fixed-head text-end">Cena enote</th>
            <th scope="col" class="fixed-head text-end">Količina</th>
            <th scope="col" class="fixed-head text-end">Cena</th>
            <th scope="col" class="fixed-head text-end">Vrednost</th>
            <th scope="col" class="fixed-head text-end">Donos</th>
          </tr>
        </thead>
        <tbody>
          % for transakcija in kriptovaluta["transakcije"]:
          <tr>
            <td class="py-0">
              {{transakcija["datum"]}}
            </td>
            <td class="py-0 text-end">
              {{f"{transakcija["cena_enote"]:.2f}"}} €
            </td>
            <td class="py-0 text-end">
              {{f"{transakcija["kolicina"]:.6f}"}}
            </td>
            % cena = transakcija["kolicina"] * transakcija["cena_enote"]
            <td class="py-0 text-end">
              {{f"{cena:.2f}"}} €
            </td>
            % vrednost = transakcija["kolicina"] * kriptovaluta["vrednost_enote"]
            <td class="py-0 text-end">
              {{f"{vrednost:.2f}"}} €
            </td>
            % donos = vrednost - cena
            <td class="py-0 text-end">
              {{f"{donos:.2f}"}} €
            </td>
          </tr>
          % end
        </tbody>
        <tfoot class="fixed-foot bg-secondary">
          <tr>
            <th scope="row" class="fiksna-vrstica">
              SKUPAJ
            </th>
            <td></td> <!-- cena enote -->
            <td class="fixed-foot text-end">
              {{f"{skupna_kolicina:.6f}"}}
            </td>
            <td class="fixed-foot text-end">
              {{f"{skupna_cena:.2f}"}} €
            </td>
            <td class="fixed-foot text-end">
              {{f"{skupna_vrednost:.2f}"}} €
            </td>
            <td class="fixed-foot text-end">
              {{f"{skupen_donos:.2f}"}} €
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
    <div class="row mb-3" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/">Posodobi stanje</a>
      </div>
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/">Dodaj novo transakcijo</a>
      </div>
    </div>
  </div>
</div>