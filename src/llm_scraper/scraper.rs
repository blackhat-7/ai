use anyhow::Result;
use reqwest;
use serde::Deserialize;

// use pyo3::prelude::*;
// use pyo3_ffi::c_str;

pub struct Scraper {
    crawl4ai_endpoint: String,
}

#[derive(Debug, Clone, Deserialize)]
pub struct ScrapeResult {}

impl Scraper {
    pub fn new(crawl4ai_endpoint: String) -> Self {
        Scraper { crawl4ai_endpoint }
    }

    pub async fn scrape(&self, url: &str) -> Result<ScrapeResult> {
        let client = reqwest::Client::new();
        let res = client
            .get(&self.crawl4ai_endpoint)
            .query(&[("url", url)])
            .send()
            .await?;
        let text = res.text().await?;
        Ok(serde_json::from_str(&text)?)
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
