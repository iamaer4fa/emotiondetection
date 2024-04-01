package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"os/exec"
)

func runPythonScript(w http.ResponseWriter, r *http.Request) {

	audioFile, err := os.CreateTemp("", "recorded_audio*.wav")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer audioFile.Close()

	soxAudio := "C:\\Program Files (x86)\\sox-14-4-2\\sox.exe"
	cmd := exec.Command("cmd.exe", "/c", soxAudio, "-t", "waveaudio", "0", audioFile.Name(), "trim", "0", "4")

	err = cmd.Run()
	if err != nil {
		print("Error recording audio. %", err.Error())
	}

	venvActivatePath := "C:\\emotionapp\\emotion\\Scripts\\Activate.bat"
	pythonScriptPath := "C:\\emotionapp\\emotion\\Lib\\site-packages\\deep_audio_features\\bin\\basic_test.py"
	emotionModel := "pkl\\model_all.pt"

	// python Lib\site-packages\deep_audio_features\bin\basic_test.py -m pkl\model_all.pt -i input\this-is-how-it-ends-260306.wav

	cmd = exec.Command("cmd.exe", "/c", venvActivatePath, "&&", "python ", pythonScriptPath, " -m", emotionModel, " -i", audioFile.Name())
	stdout, err := cmd.Output()

	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	fmt.Fprintf(w, "Python script output:\n%s", stdout)
	os.Remove(audioFile.Name())

	// Set the environment variable if your venv requires it
	// cmd.Env = append(os.Environ(), "PYTHONPATH=C:\\emotionapp")

	data := struct {
		ScriptOutput string
	}{
		ScriptOutput: string(stdout),
	}

	tmpl, err := template.ParseFiles("templates/index.html")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	err = tmpl.Execute(w, data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

}

func main() {
	http.HandleFunc("/run_script", runPythonScript)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
