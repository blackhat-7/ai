package utils

import (
	"bufio"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strings"
)

var (
	PathNotFound = errors.New("path not found")
)

func Which(path string) (string, error) {
	cmd := exec.Command("which", path)
	output, err := cmd.Output()
	if err != nil {
		return "", PathNotFound
	}
	return strings.TrimSpace(string(output)), nil
}

func CopyFile(src, dst string) error {
	sourceFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer sourceFile.Close()

	// Create or truncate destination file
	destFile, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer destFile.Close()

	// Copy contents
	_, err = io.Copy(destFile, sourceFile)
	return err
}

func InstallPythonLibs(pythonPath string, libNames []string) error {
	cmd := exec.Command(pythonPath, "-m", "pip", "install", "--upgrade", strings.Join(libNames, " "))
	stdout, _ := cmd.StdoutPipe()
	stderr, _ := cmd.StderrPipe()
	cmd.Start()
	scanner := bufio.NewScanner(stdout)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
	scanner = bufio.NewScanner(stderr)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
	}
	if err := cmd.Wait(); err != nil {
		return fmt.Errorf("failed to install Python library: %w", err)
	}
	return nil
}
