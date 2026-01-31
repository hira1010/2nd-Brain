import { AbsoluteFill } from 'remotion';

export const MyComposition = () => {
    return (
        <AbsoluteFill
            style={{
                justifyContent: 'center',
                alignItems: 'center',
                backgroundColor: 'white',
                fontSize: 80,
            }}
        >
            Hello World!
        </AbsoluteFill>
    );
};
