import enTranslations from "@shopify/polaris/locales/en.json";
import { AppProvider, Page, Card, Button, DataTable } from "@shopify/polaris";
import { useState, useEffect, useCallback } from "react";

function App() {
  console.log("Render");
  const [productsAll, setProductsAll] = useState(null);
  const [productsAllRows, setProductsAllRows] = useState([]);

  useEffect(() => {
    async function fetchData() {
      
      await fetch("http://mlbot.startpunkt.co:3000/products-all.json").then(
        (e) =>
          e.json().then((e) => {
            setProductsAll(null)
            setProductsAllRows([])
            setProductsAll(e);
            e.forEach((v, i) => {
              var thisRow = [v.growth_rate, v.total_sales, <a href={v.URL} target="_blank">Link</a>];

              setProductsAllRows((prev) => [...prev, thisRow]);
            });
          })
      );
    }
    fetchData();
  }, []);
  const sortNumber = (rows, index, direction) =>{
    return [...rows].sort((rowA, rowB) => {
      const amountA = rowA[index];
      const amountB = rowB[index];
      

      return direction === 'descending' ? amountB - amountA : amountA - amountB;
    });

  }
   const handleSort = useCallback(
    (index, direction) => setProductsAllRows(sortNumber(productsAllRows, index, direction)),
    [productsAllRows],
  );
  console.log(productsAllRows);
  return (
    <AppProvider i18n={enTranslations}>
      <Page title="Mercado Libre Bot By Tony Gonzalez">
        <Card sectioned>
        {productsAllRows != null ?
        <DataTable
          columnContentTypes={[                      
            'text',
            'text',    
            "text"        
          ]}
          headings={[                     
            'Crecimiento Ventas',
            'Ventas Totales',
            "Link"            
          ]}
          rows={productsAllRows}
          sortable={[true, true, false]}
          onSort={handleSort}
          />
          : null
        }
        </Card>
      </Page>
    </AppProvider>
  );
}

export default App;
