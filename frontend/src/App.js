import './App.css';
import React, { useCallback, useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";

const CameraComponent = () => {
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [isPortrait, setIsPortrait] = useState(window.innerHeight > window.innerWidth);

  // Handle orientation changes
  useEffect(() => {
    const handleOrientationChange = () => {
      setIsPortrait(window.innerHeight > window.innerWidth);
    };

    window.addEventListener('resize', handleOrientationChange);
    return () => window.removeEventListener('resize', handleOrientationChange);
  }, []);

  const videoConstraints = {
    width: { min: 640, ideal: 1920, max: 1920 },
    height: { min: 480, ideal: 1080, max: 1080 },
    facingMode: 'environment'
  };

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef]);

  const retake = () => {
    setImgSrc(null);
  };

  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      width: '100vw',
      position: 'fixed',
      top: 0,
      left: 0,
      backgroundColor: '#000'
    },
    camera: {
      width: '100%',
      height: '100%',
      objectFit: 'contain',
      transform: isPortrait ? 'none' : 'rotate(90deg)',
      transition: 'transform 0.3s ease'
    },
    buttonContainer: {
      position: 'fixed',
      bottom: '20px',
      width: '100%',
      display: 'flex',
      justifyContent: 'center',
      padding: '20px',
      zIndex: 1
    },
    button: {
      padding: '15px 30px',
      fontSize: '18px',
      borderRadius: '25px',
      border: 'none',
      backgroundColor: '#fff',
      color: '#000',
      boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
    },
    preview: {
      width: '100%',
      height: '100%',
      objectFit: 'contain'
    }
  };

  return (
    <div style={styles.container}>
      {imgSrc ? (
        <img src={imgSrc} alt="captured" style={styles.preview} />
      ) : (
        <Webcam
          ref={webcamRef}
          audio={false}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
          style={styles.camera}
        />
      )}
      <div style={styles.buttonContainer}>
        {imgSrc ? (
          <button onClick={retake} style={styles.button}>Retake</button>
        ) : (
          <button onClick={capture} style={styles.button}>Capture</button>
        )}
      </div>
    </div>
  );
};

export default CameraComponent;
