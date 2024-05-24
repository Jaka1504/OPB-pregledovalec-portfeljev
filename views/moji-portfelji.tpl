% rebase("base.tpl", title="Moji portfelji")


<h1>Moji portfelji</h1>
<div class="card bg-secondary">
  <div class="card-header">
    <p class="mb-0">
      Kliknite na gumb na desni za podrobnejši vpogled ali urejanje posameznega portfelja.
    </p>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead class="fixed-head bg-secondary">
          <tr>
            <th scope="col" class="fixed-head">Ime</th>
            <th scope="col" class="fixed-head text-end">Cena</th>
            <th scope="col" class="fixed-head text-end">Vrednost</th>
            <th scope="col" class="fixed-head text-end">Donos</th>
            <th scope="col" class="fixed-head text-end">Trend</th>
            <th scope="col" class="fixed-head text-end">Vpogled</th>
          </tr>
        </thead>
        <tbody>
          % for portfelj in portfelji:
          <tr>
            <th scope="row">
              {{portfelj["ime"]}}
            </th>
            <td class="text-end">
              {{round(portfelj["cena"], 2)}} €
            </td>
            <td class="text-end">
              {{round(portfelj["vrednost"], 2)}} €
            </td>
            <td class="text-end">
              {{round(portfelj["donos"], 2)}} €
            </td>
            <td class="text-end">
              % if portfelj["trend"] >= 0: 
              <span class="besedilo-zeleno">{{round(portfelj["trend"], 2)}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{round(portfelj["trend"], 2)}} % ▼</span>
              % end
            </td>
            <td class="text-end text-light">
              <a class="btn btn-outline-light m-0 px-3 py-0" href="/moji-portfelji/{{portfelj['id']}}">
                <img src="/img/search.svg" class="invert"></img>
              </a>
            </td>
          </tr>
          % end
        </tbody>
        <tfoot class="fixed-foot bg-secondary">
          <tr>
            <th scope="row" class="fixed-foot">
              SKUPAJ
            </th>
            <td class="fixed-foot text-end">
              {{round(sum([portfelj["cena"] for portfelj in portfelji]), 2)}} €
            </td>
            <td class="fixed-foot text-end">
              % skupna_vrednost = sum([portfelj["vrednost"] for portfelj in portfelji])
              {{round(skupna_vrednost, 2)}} €
            </td>
            <td class="fixed-foot text-end">
              {{round(sum([portfelj["donos"] for portfelj in portfelji]), 2)}} €
            </td>
            <td class="fixed-foot text-end">
              % skupen_trend = round(sum([portfelj["trend"] * portfelj["vrednost"] for portfelj in portfelji]) / skupna_vrednost, 2)
              % if skupen_trend >= 0: 
              <span class="besedilo-zeleno">{{skupen_trend}} % ▲</span>
              % else:
              <span class="besedilo-rdece">{{skupen_trend}} % ▼</span>
              % end
            </td>
            <td class="fixed-foot">
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
        <a class="btn btn-dark btn-block" href="/">Dodaj nov portfelj</a>
      </div>
    </div>
  </div>
</div>