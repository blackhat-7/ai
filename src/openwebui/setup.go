package openwebui

import (
	"ai/src/utils"
	"fmt"
	"strings"
)

const (
	// PythonLibraries is a list of Python libraries to install
	PythonLibraries = "open-webui"
)

func Setup() error {
	// get python path
	pythonPath, err := utils.Which("python")
	if err != nil {
		return err
	}

	// install Python libraries
	if err = utils.InstallPythonLibs(pythonPath, strings.Split(PythonLibraries, " ")); err != nil {
		return fmt.Errorf("failed to install Python libraries: %w", err)
	}

	return nil
}
