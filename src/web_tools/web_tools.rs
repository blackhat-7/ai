use std::f32::consts::E;

use reqwest;
use serde::Deserialize;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum WebToolsError {
    #[error("General error: {0}")]
    GeneralError(String),
}

#[derive(Debug, Deserialize)]
pub struct SearchResult {
    url: String,
    title: String,
    content: String,
}

pub struct WebTools {
    crawl4ai_endpoint: String,
}

pub struct SearchQuery {
    query: String,
    time_range: Option<String>,
    website: Option<String>,
}

impl WebTools {
    pub fn new(crawl4ai_endpoint: String) -> Self {
        WebTools { crawl4ai_endpoint }
    }

    pub async fn search(&self, query: SearchQuery) -> Result<Vec<SearchResult>, WebToolsError> {
        let mut query_params: Vec<(&str, &str)> = vec![("query", &query.query)];

        if let Some(ref time_range) = query.time_range {
            query_params.push(("time_range", time_range));
        }

        if let Some(ref website) = query.website {
            query_params.push(("website", website));
        }

        let client = reqwest::Client::new();
        let res = client
            .get(&self.crawl4ai_endpoint)
            .query(&query_params)
            .send()
            .await
            .map_err(|e| WebToolsError::GeneralError(e.to_string()))?;

        let text = res
            .text()
            .await
            .map_err(|e| WebToolsError::GeneralError(e.to_string()))?;
        let search_results: Vec<SearchResult> =
            serde_json::from_str(&text).map_err(|e| WebToolsError::GeneralError(e.to_string()))?;
        Ok(search_results)
    }

    // pub fn scrape_py() -> PyResult<()> {
    //     let py_foo = c_str!(include_str!(concat!(
    //         env!("CARGO_MANIFEST_DIR"),
    //         "/python_app/utils/foo.py"
    //     )));
    //     let py_app = c_str!(include_str!(concat!(
    //         env!("CARGO_MANIFEST_DIR"),
    //         "/python_app/app.py"
    //     )));
    //     let from_python = Python::with_gil(|py| -> PyResult<Py<PyAny>> {
    //         PyModule::from_code(py, py_foo, c_str!("utils.foo"), c_str!("utils.foo"))?;
    //         let app: Py<PyAny> = PyModule::from_code(py, py_app, c_str!(""), c_str!(""))?
    //             .getattr("run")?
    //             .into();
    //         app.call0(py)
    //     });

    //     println!("py: {}", from_python?);
    //     Ok(())
    // }
}
