package it.emarolab.sit;

import it.emarolab.sit.owloopDescriptor.SceneClassDescriptor;

import java.util.Comparator;

public class TestSceneReverseOrder implements Comparator<SceneClassDescriptor> {

    @Override
    public int compare(SceneClassDescriptor t, SceneClassDescriptor t1) {
        return Integer.compare(t1.getCardinality(),t.getCardinality());
    }
}
