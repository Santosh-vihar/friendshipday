    from pathlib import Path

    import numpy as np
    from moviepy.editor import AudioFileClip, CompositeVideoClip, ImageClip, TextClip, concatenate_videoclips


    def _create_silent_audio(duration):
        from moviepy.audio.AudioClip import AudioClip

        def make_frame(_time):
            return np.zeros((1, 2))

        return AudioClip(make_frame, duration=duration, fps=44100)


    def create_slideshow(image_paths, name, output_path, bg_music_path=None, duration_per_image=3.0, crossfade_duration=1.0):
        clips = []
        for image_path in image_paths:
            clip = ImageClip(image_path).set_duration(duration_per_image).resize(lambda time: 1 + 0.05 * time).set_position("center")
            clips.append(clip)

        video = concatenate_videoclips(clips, method="compose", padding=-crossfade_duration)

        txt_title = (
            TextClip(
                f"Happy Friendship Day, {name}",
                fontsize=60,
                color="white",
                font="Liberation-Sans",
                stroke_color="black",
                stroke_width=2,
                method="label",
            )
            .set_duration(2)
            .set_position("center")
            .crossfadein(0.5)
        )

        end_msg = (
            TextClip(
                f"Thank you, {name} ❤️
From Vihar",
                fontsize=50,
                color="white",
                font="Liberation-Sans",
                stroke_color="black",
                stroke_width=2,
                method="label",
                align="center",
            )
            .set_duration(3)
            .set_position("center")
            .crossfadein(0.5)
        )

        final_video = CompositeVideoClip([video, txt_title.set_start(0), end_msg.set_start(video.duration - 3)])

        if bg_music_path and Path(bg_music_path).exists():
            audio = AudioFileClip(bg_music_path).subclip(0, final_video.duration).volumex(0.3)
        else:
            audio = _create_silent_audio(final_video.duration)

        final_video = final_video.set_audio(audio)
        final_video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            threads=4,
            preset="medium",
            verbose=False,
            logger=None,
        )
