use anyhow::{anyhow, Result};
use serde::Deserialize;
use serde_json;
use std::{
    path::{Path, PathBuf},
    process::Command,
};

use crate::utils;

pub fn backup(backup_dir: &impl AsRef<Path>) -> Result<()> {
    let db_name = "webui.db";
    let backup_dir = backup_dir.as_ref();
    if !backup_dir.exists() {
        std::fs::create_dir(backup_dir)?;
    }
    let backup_db_path = backup_dir.join(db_name);
    if backup_db_path.exists() {
        return Err(anyhow!("db already exists in the given path"));
    }
    let owui_db_path = get_owui_db_path()?;

    std::fs::copy(owui_db_path, backup_dir)?;
    Ok(())
}

#[derive(Deserialize)]
pub struct SitePaths {
    paths: Vec<String>,
}

fn get_python_site_packages_paths(python_path: &impl AsRef<Path>) -> Result<Vec<PathBuf>> {
    let python_path = python_path.as_ref();
    let output = Command::new(python_path)
        .arg(python_path)
        .arg("-c")
        .arg("import site, json; print(json.dumps(site.getsitepackages()))")
        .output()?;
    let jstring = String::from_utf8(output.stdout)?;
    let paths: SitePaths = serde_json::from_str(&jstring)?;
    Ok(paths.paths.into_iter().map(PathBuf::from).collect())
}

fn get_owui_db_path() -> Result<PathBuf> {
    let python_path = utils::which("python")?;
    let site_packages_paths = get_python_site_packages_paths(&python_path)?;
    let mut owui_db_paths: Vec<PathBuf> = site_packages_paths
        .iter()
        .filter_map(|p| {
            let db_path = p.join("open_webui").join("data").join("webui.db");
            if db_path.exists() {
                return Some(db_path);
            }
            return None;
        })
        .collect();
    if owui_db_paths.len() == 0 {
        return Err(anyhow!("no owui db in site pacakges"));
    } else if owui_db_paths.len() > 1 {
        return Err(anyhow!("multiple owui db in site pacakges"));
    }
    Ok(owui_db_paths.pop().unwrap())
}
