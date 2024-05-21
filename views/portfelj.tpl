% rebase("base.tpl", title="Portfelj " + portfelj["ime"])


<h1>Portfelj {{portfelj["ime"]}}</h1>
<div class="card bg-secondary">
  <div class="card-header">
    <p class="mb-0">
      Kliknite na gumb na desni za podrobnejši vpogled ali urejanje posamezne transakcije.
    </p>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead>
          <tr>
            <th scope="col">Sredstvo</th>
            <th scope="col">Kratica</th>
            <th scope="col">Datum nakupa</th>
            <th scope="col">Količina</th>
            <th scope="col" class="text-end">Cena</th>
            <th scope="col" class="text-end">Vrednost</th>
            <th scope="col" class="text-end">Donos</th>
            <th scope="col" class="text-end">Trend</th>
            <th scope="col" class="text-end">Vpogled</th>
          </tr>
        </thead>
        <tbody>
          % for transakcija in portfelj["transakcije"]:
          <tr>
            <th scope="row">
              {{transakcija["sredstvo"]}}
            </th>
            <td>
              {{transakcija["kratica"]}}
            </td>
            <td>
              {{transakcija["datum"]}}
            </td>
            <td class="text-end">
              {{transakcija["kolicina"]}}
            </td>
            <td class="text-end">
              {{transakcija["cena"]}} €
            </td>
            <td class="text-end">
              {{transakcija["vrednost"]}} €
            </td>
            <td class="text-end">
              {{transakcija["donos"]}} €
            </td>
            <td class="text-end">
              % if transakcija["trend"] >= 0: 
              <span class="besedilo-zeleno">{{transakcija["trend"]}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{transakcija["trend"]}} % ▼</span>
              % end
            </td>
            <td class="text-end text-light">
              <a class="btn btn-outline-light m-0 px-3 py-0" href="/transakcija/{{transakcija['id']}}">
                <img src="/img/search.svg" class="invert"></img>
              </a>
            </td>
          </tr>
          % end
          <tr>
            <th scope="row">
              SKUPAJ
            </th>
            <td></td> <!-- kratica -->
            <td></td> <!-- datum -->
            <td></td> <!-- kolicina -->
            <td class="text-end">
              {{sum([transakcija["cena"] for transakcija in portfelj["transakcije"]])}} €
            </td>
            <td class="text-end">
              % skupna_vrednost = sum([transakcija["vrednost"] for transakcija in portfelj["transakcije"]])
              {{skupna_vrednost}} €
            </td>
            <td class="text-end">
              {{sum([transakcija["donos"] for transakcija in portfelj["transakcije"]])}} €
            </td>
            <td class="text-end">
              % skupen_trend = round(sum([transakcija["trend"] * transakcija["vrednost"] for transakcija in portfelj["transakcije"]]) / skupna_vrednost, 2)
              % if skupen_trend >= 0: 
              <span class="besedilo-zeleno">{{skupen_trend}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{skupen_trend}} % ▼</span>
              % end
            </td>
            <td></td> <!-- vpogled -->
          </tr>
        </tbody>
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