package openwebui

import (
	"ai/src/utils"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

func Backup(backupPath string) error {
	// check if backup dir exists
	if _, err := os.Stat(backupPath); os.IsNotExist(err) {
		if err := os.Mkdir(backupPath, 0755); err != nil {
			return fmt.Errorf("Failed to create backup directory: %w", err)
		}
	}

	// get python path
	pythonPath, err := utils.Which("python")
	if err != nil {
		return fmt.Errorf("Failed to find python executable: %w", err)
	}

	// get sitepackages path
	sites, err := getPythonSitePackagesPath(pythonPath)
	if err != nil {
		return fmt.Errorf("Failed to get site packages path: %w", err)
	}

	owuiDbPaths := []string{}
	for _, site := range sites {
		tempPath := filepath.Join(site, "open_webui", "data", "webui.db")
		// check if file exists
		if _, err := os.Stat(tempPath); err != nil {
			continue
		}
		owuiDbPaths = append(owuiDbPaths, tempPath)
	}

	if len(owuiDbPaths) == 0 {
		return fmt.Errorf("No open_webui database found in site packages for python %s", pythonPath)
	} else if len(owuiDbPaths) > 1 {
		return fmt.Errorf("Multiple open_webui databases found in site packages for python %s: %+v", pythonPath, owuiDbPaths)
	}

	// we have only 1 db to backup
	owuiDbPath := owuiDbPaths[0]

	// copy file to backup dir
	if err := utils.CopyFile(owuiDbPath, filepath.Join(backupPath, "webui.db")); err != nil {
		return fmt.Errorf("Failed to copy open_webui database to backup directory: %w", err)
	}

	return nil

}

func getPythonSitePackagesPath(pythonPath string) ([]string, error) {
	// get sitepackages path
	cmd := exec.Command(pythonPath, "-c", "import site, json; print(json.dumps(site.getsitepackages()))")
	output, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("command %s failed: %w", cmd.String(), err)
	}
	sitesStr := strings.TrimSpace(string(output))
	var sites []string
	if err := json.Unmarshal([]byte(sitesStr), &sites); err != nil {
		return nil, fmt.Errorf("Failed to parse site packages path %s: %w", sitesStr, err)
	}
	return sites, nil
}
