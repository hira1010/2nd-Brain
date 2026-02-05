import { Composition } from 'remotion';
import { JimiPV } from './JimiPV';

export const RemotionRoot = () => {
    return (
        <>
            <Composition
                id="JimiPV"
                component={JimiPV}
                durationInFrames={1800}
                fps={30}
                width={1920}
                height={1080}
            />
        </>
    );
};
